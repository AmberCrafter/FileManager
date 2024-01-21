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
        - rulename: 
            - type: file class
            - format: reguler expersion for filting files, which can provide parameter to folder
            - folder: folder structure
            - labels: metadata for this file which used for search system
                - filename: base on filename information
                - [Optional] metadata: netcdf metadata information
            - plugin: helper function for handling operations
            - cache_path: cache file path

## Todo
- [x] search system
    - [x] SQLite
    - [x] Auto add metadata
- [x] file duplicate
    - [ ] ~~~raise error~~~
    - [x] log warning
    - [x] setup Filesystem config
- [x] default rule for unknown type
    - [x] skip it and show error message
- [x] file tages
- [x] load config & cache & module
- [ ] Add configuration manager
    - [ ] ConfigFinder inherit from ConfigManger
