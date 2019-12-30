from log import Logger, LOG_LEVELS, set_level

def test_logger():
    log1 = Logger("test1")
    assert log1.level == LOG_LEVELS['info']
    log1.info("test1: printing on info")
    log1.debug("test1: should not print")
    set_level(log1.logger, "debug")
    assert log1.level == LOG_LEVELS['debug']
    log1.debug("test1: should print on debug")

    Logger.LOG_LEVEL = "warning"
    log2 = Logger("test2")
    assert id(log1) == id(log2)
    assert log2.level == LOG_LEVELS['warning']
    log2.warning("test2: should print on warning")
    assert log1.level == LOG_LEVELS['warning']
    log1.info("test1: does not print anymore!")

    Logger.LOG_LEVEL = "asdasd"
    log3 = Logger("test3")
    assert log3.level == LOG_LEVELS['info']
    assert id(log1) == id(log2) == id(log3)
    log3.info("log3: should print on info")
