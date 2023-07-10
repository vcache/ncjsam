#!/usr/bin/env python3
# python3 -m http.server --bind 127.0.0.1


from ncjsam.tool import main
from requirements import perform_test


if __name__ == '__main__':
    perform_test()
    main.run()
