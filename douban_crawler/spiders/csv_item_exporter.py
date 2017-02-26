# -*- coding: utf-8 -*-
from scrapy.conf import settings
#from scrapy.contrib.exporter import CsvItemExporter
from scrapy.exporters import CsvItemExporter

class TagCsvItemExporter(CsvItemExporter):
    def __init__(self, *args, **kwargs):
        delimiter = settings.get('CSV_DELIMITER', ',')
        kwargs['delimiter'] = delimiter
        kwargs['include_headers_line']=True
        fields_to_export = settings.get('FIELDS_TO_EXPORT', [])
        if fields_to_export :
            kwargs['fields_to_export'] = fields_to_export
            super(TagCsvItemExporter, self).__init__(*args, **kwargs)

