# WebTracker
Tracks and monitors Website Changes 

## Installation
```bash
pip install -r requirements.txt
```

## Configuration
Change the `WEBHOOK_URL` in `tracker.py` to your Discord Webhook URL
```
WEBHOOK_URL = "<YOUR_WEBHOOK_URL>"
```

## Usage
Save your urls in `urls.txt` file
```txt
https://www.google.com
https://www.youtube.com
```

Run the script
```bash
python tracker.py
```

## License
[MIT](https://choosealicense.com/licenses/mit/)