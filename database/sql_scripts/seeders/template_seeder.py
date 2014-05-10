import os
import csv
import json

from tables.templates import (
    ResponseTemplate
)

from seeders.base_seeder import BaseSeeder, print_delete_count

class TemplateSeeder(BaseSeeder):
    def seed(self):
        self.clear_templates()
        for response_path in os.listdir(self.template_data):
            with open(os.path.join(self.template_data, response_path), 'r') as file_:
                templates = json.loads(file_.read())
                for template in templates:
                    print("Adding template for response %s" % template)
                    JSONstr = json.dumps(templates[template])
                    new_template = ResponseTemplate(name=template, json=JSONstr)
                    self.session.add(new_template)

    def clear_templates(self):
        print("Clearing all template tables")
        print_delete_count(self.session.query(ResponseTemplate).delete())


