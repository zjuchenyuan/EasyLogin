# coding=utf-8
import os
if "runonly" in os.environ: # pragma: no cover
    flag = False
else:
    os.environ["runonly"] = ""
    flag = True
if flag or "main" in os.environ["runonly"]:
    from .test_main import TestMain
if flag or "httpbin" in os.environ["runonly"]:
    from .test_httpbin import TestHttpbin
if flag or "panzju" in os.environ["runonly"]:
    from .test_panzju import TestPanzju