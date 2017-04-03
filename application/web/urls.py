from .views import *

url = {
    "^/$": sub_view_func_test,
    "^/sub/?$": sub_view_func_test_2,
}
