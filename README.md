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
    "actions": ["list", "of" "string"] (OPTIONS: "video", "crop", "ai" or "")
},
```
