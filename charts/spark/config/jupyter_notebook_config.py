c = get_config()
c.NotebookApp.ip = '0.0.0.0'
c.NotebookApp.port = 8888
c.NotebookApp.open_browser = False
c.NotebookApp.base_url = '/pyspark'
c.NotebookApp.password = 'sha1:2cd248f70b21:4ed6830be3936126616f12c006487363092b4c4c'