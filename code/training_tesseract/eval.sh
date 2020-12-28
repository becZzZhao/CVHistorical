  
lstmeval \
--model TNR.lstm \
--load_images test/jpg/* \
--traineddata tesseract/tessdata/eng.traineddata \
--eval_listfile train/eng.training_files.txt

# --model output/TNR_checkpoint \
# --traineddata output/TNR.traineddata \
# --eval_listfile train/eng.training_files.txt