# image_treatment
##Mfdata project to download image and video streams of road to analyse it with IA technology.


###JSON convention:

```
"name of dict (same as the camera name or more precise)":
{
    "name":"string" (NOT EMPTY),
    "url": "string" (NOT EMPTY),
    "http_referer": "string" (OPTIONAL),
    "location": "lat long" (NOT EMPTY),
    "crop_x": "string of int", (if action["crop"] NOT EMPTY)
    "crop_y": "string of int", (if action["crop"] NOT EMPTY)
    "crop_width": "string of int", (if action["crop"] NOT EMPTY)
    "crop_height": "string of int", (if action["crop"] NOT EMPTY)
    "actions": ["list", "of", "string"] (OPTIONS: "video", "crop", "ai" or "")
}
```

###Detail of actions parameters:

- *video* is used when the url reaches a video by default jpg are treated. (linked with video.py)
- *crop* allows to crop an image accordingly to the crop parameters to give. (linked with crop.py)
- *ai* is the final action that will treat image with ai and send images and information to the database. (linked with ai_result.py)
