# SwinHackathon
Prerequisite step:
```
pip install -r requirements.txt
```
Steps:
- Install Redis
- Run command : 
```
celery -A celery_config worker --pool=solo -l info
python main.py
```
