import logging
def setup_logger(output_dir):
    output_dir.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("hidden_url_finder")
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        fmt = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
        fh = logging.FileHandler(output_dir / "run.log", encoding="utf-8")
        fh.setFormatter(fmt)
        sh = logging.StreamHandler()
        sh.setFormatter(fmt)
        logger.addHandler(fh); logger.addHandler(sh)
    return logger
