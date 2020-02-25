# Imports
import xml.etree.ElementTree as ET


class WatsonXmlGenerator:

    def __init__(self):
        self.left = '<Envelope><Body>'
        self.right = '</Body></Envelope>'

    def __str__(self):
        return f'XML generator for IBM Watson Campaign Automation XML API'

    def __wrap(self, xml):
        f'{self.left}{xml}{self.right}'

    def calculate_query(self, query_id):
        xml = f'<CalculateQuery><QUERY_ID>{query_id}</QUERY_ID></CalculateQuery>'
        return self.__wrap(xml)

    def job_status_check(self, job_id):
        xml = f'<GetJobStatus><JOB_ID>{job_id}</JOB_ID></GetJobStatus>'
        return self.__wrap(xml)

    def export_query(self, target_id,
                     columns,
                     export_format='CSV',
                     export_type='ALL'):
        if isinstance(columns, list):
            if 'EMAIL' not in columns:
                columns.append('EMAIL')
            if 'RECIPIENT_ID' not in columns:
                columns.append('RECIPIENT_ID')
            xml = f'<LIST_ID>{target_id}</LIST_ID>'
            xml += f'<EXPORT_TYPE>{export_type}</EXPORT_TYPE>'
            xml += f'<EXPORT_FORMAT>{export_format}</EXPORT_FORMAT>'
            xml += f'<EXPORT_COLUMNS>'
            xml += ''.join([f'<COLUMN>{column}</COLUMN>' for column in columns])
            xml += f'</EXPORT_COLUMNS>'
            return self.__wrap(f'<ExportList>{xml}</ExportList>')
        else:
            return f'Variable columns must be a list'

    def purge_data(self, target_id, source_id):
        xml = f'<TARGET_ID>{target_id}</TARGET_ID><SOURCE_ID>{source_id}</SOURCE_ID></PurgeData>'
        return self.__wrap(xml)
