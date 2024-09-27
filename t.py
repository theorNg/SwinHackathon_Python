from ultralytics import YOLO

model = YOLO('best_weight.pt')

results = model.predict('test.jpg', save = True)
# for result in results:
        
