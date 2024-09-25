import json
import requests 

def publish_image():
    access_token="EAAH6NKLPk1gBO9EaXCwV7A07nZBTFbZBF184m7sxfvsxPZB5WMHpkDUS8lR0ZB0NPXygaGWp1DpMbVYFBcuGtYFcDaFhSfWKN9kofRHsLxvldlUt9T1LP5Wudul1smSrXajHRjVT6hum809aCUw0UxNth0ePjq95MpVdJZBjFJHkw4PCiVZAxmNnLZClEq6xlXT"
    ig_user_id = "17841469368208142"
    img_url="https://images.pexels.com/photos/122383/pexels-photo-122383.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"

    post_url=f"https://graph.facebook.com/v20.0/{ig_user_id}/media"

    payload={
        "image_url":img_url,
        "caption":"Respect the Nature",
        "access_token":access_token
    }
    r=requests.post(post_url,data=payload)
    print(r.text)
    print("Post uploaded successfully")

    results = json.loads(r.text)

    if 'id' in results:
        creation_id=results['id']
        second_url=f"https://graph.facebook.com/v20.0/{ig_user_id}/media_publish"
        second_payload={
            'creation_id':creation_id,
            'access_token':access_token
        }
        r=requests.post(second_url,data=second_payload)
        print(r.text)
        print("image published to instagram")
    else:
        print("image not hosted")
publish_image()
