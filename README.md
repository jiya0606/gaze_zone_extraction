Given a video from the driver's view and a corresponding CSV with gaze location, the code will extract individual images based on the given time frames in the CSV. It will then crop these images based on a radius of focus, with the center being at the [x,y] coordinates of the driver's gaze. Lastly, computer vision classification will be used to classify these cropped images into the zones depicted in the image below and save this information into a few CSV file.


<img width="496" alt="Screenshot 2024-06-03 at 5 04 43 PM" src="https://github.com/jiya0606/gaze_zone_extraction/assets/79244584/1df65fbf-0ba6-4995-9235-39894c96a5c0">
