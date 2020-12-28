./tesstrain.sh --lang eng --fonts_dir fonts\
        --fontlist 'Times New Roman'\
        --lang eng \
        --linedata_only \
        --langdata_dir tesseract/langdata_lstm \
        --tessdata_dir tesseract/tessdata \
        --save_box_tiff \
        --maxpages 20 \
        --output_dir train