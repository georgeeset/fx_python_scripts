
def check_pattern():
    #TODO move the below block to daily activity as it is needed there
    try:
        pattern_detector.check_patterns(data, item[constants.TABLE])
    except Exception as e:
        logging.error(f"pattern detection failed: {e}")
        print(f"error detecting pattern {e}")
    # delete old data from support/resistance history


if __name__ == "__main__":
    check_pattern()