import azure.functions as func
import logging
import logging
import azure.functions as func
from services.db_util import insertData
from services.serviceUtils import extract_text_from_html
from services.llm_api import summarize_and_tag

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="cri_hack")
def cri_hack(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "~ Wishing you a great day ahead !!! ~ Divakar",
             status_code=200  
        )
    
@app.route(route="subscribe" , methods=["POST"])
def subscribe(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    email = req.params.get('email')
    tags = req.params.get('tags') # this must be a comma-separated string of tags 
    if not email:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            email = req_body.get('email')

    if email:
        return func.HttpResponse(f"Subscription successful for {email}.")
    else:
        return func.HttpResponse(
            "Please provide a valid email address.",
            status_code=400
        )

@app.route(route="test_diva")
def appendData(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    try:
        return insertData(req)
    except Exception as e:
        return func.HttpResponse(f"Error: {str(e)}", status_code=500)
    
@app.route(route="create_summary_and_tags", methods=["POST"])
def create_summary_and_tags(req: func.HttpRequest) -> func.HttpResponse:
    logging.info(f"Processing request for summary and tags.")
    try:
        req_body = req.get_json()
        logging.info(f"Request body: {req_body}")

        post = req_body.get("post", {})
        replies = req_body.get("replies", [])

        # Extract main post details
        post_id = post.get("id")
        author = post.get("author")
        date_time = post.get("dateTime")
        content = extract_text_from_html(post.get("content") or "")
        url = post.get("url")
        title = post.get("subject", "No Title")

        logging.info(f"Main post - id: {post_id}, author: {author}, dateTime: {date_time}, url: {url}")
        # Get the dateTime of the first reply if available
        first_reply_time = replies[0].get("createdDateTime") if replies and "createdDateTime" in replies[0] else "No replies"
        logging.info(f"First reply dateTime: {first_reply_time}")
        # Extract replies details
        reply_summaries = []
        for reply in replies:
            
            reply_id = reply.get("id")
            reply_author = reply["from"]["user"]["displayName"] if reply.get("from") and reply["from"].get("user") and reply["from"]["user"].get("displayName") else "Unknown"
            reply_date_time = reply.get("createdDateTime")
            first_reply_time = min(first_reply_time, reply_date_time) if first_reply_time != "No replies" else reply_date_time
            reply_content = reply.get("body", {}).get("content", "")
            reply_summaries.append({
            "author": reply_author,
            "dateTime": reply_date_time,
            "content": extract_text_from_html(reply_content)
            })
            logging.info(f"Reply - id: {reply_id}, author: {reply_author}, dateTime: {reply_date_time}")
        json_data = {'post': {
                        'author': author,
                        'dateTime': date_time,
                        'content': content,
                        'title': title,
                        'url': url
                    },
                    'replies': reply_summaries
                   }
        logging.info(f"Compiled JSON data for LLM: {json_data}")
        
        # call LLM API here with json_data and get summary and tags
        summary, tags, group_tag = summarize_and_tag(json_data)
        logging.info(f"LLM response - Summary: {summary}, Tags: {tags}")
        dbData = dict()
        dbData['ShortDescription'] = summary
        dbData['Tags'] = tags
        dbData['id'] = post_id
        dbData['TeamsLink'] = url
        dbData['ChannelId'] = author
        dbData['CreationTime'] = post.get("dateTime")
        dbData['GroupTag'] = group_tag
        dbData['AdoWorkItemUrl'] = "https://dev.azure.com/org/proj/_workitems/edit/101"
        dbData['MessageId'] = post_id
        
        
        
        # insert into db
        logging.info(f"Data inserted into DB: {dbData}")
        return insertData(dbData)
    except ValueError:
        return func.HttpResponse(f"Invalid JSON in request body. {dbData}", status_code=400)
    except Exception as e:
        logging.error(f"Error processing request: {str(e)}")
        return func.HttpResponse(f"Error: {str(e)}", status_code=500)