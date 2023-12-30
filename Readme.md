# File Manager
 - version: 0.1.0
 - author: Weiru Chen
 - email: flamingm321@gmail.com
 - description:
    A simple file manager.

## configuation
 - configfile: "./config.json"
 - formation:
    - root: File system root folder
    - rules: management rules
        - classification: 
            - type: file class
            - format: reguler expersion for filting files, which can provide parameter to folder
            - folder: folder structure
            - labels: metadata for this file which used for search system
                - filename: base on filename information
                - [Optional] metadata: netcdf metadata information
