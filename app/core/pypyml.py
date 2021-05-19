import os
from pprint import pprint

import yaml

from app.core.settings import Config, get_logger

logger = get_logger('CheckYml')


class CheckYml(Config):
    __OKD_PATH = os.getcwd()
    __params = []
    __development = []
    __map_info = []
    __deploy_image = {}
    __msg_error = "Something went wrong while parsing yaml file"

    def __init__(self):
        super(CheckYml, self).__init__()
        self.params = 'deploy-params.env'
        self.deploy_image = 'deploy-image.yml'
        self.development = 'development.yml'
        self.create_env()

    @property
    def okd_path(self):
        if self.pytesseract_linux:
            return self.__OKD_PATH.replace('/app/core', '/okd/')
        else:
            return self.__OKD_PATH.replace('\\app\\core', '\\okd\\')

    @property
    def map_info(self):
        return self.__map_info

    @map_info.setter
    def map_info(self, value):
        if value is None:
            raise ValueError
        elif not isinstance(value, (dict,)):
            raise TypeError("process_result must be list")
        self.__map_info.append(value)

    @property
    def params(self):
        return self.__params

    @params.setter
    def params(self, value):
        value = f'{self.okd_path}{value}'
        try:
            with open(value) as file:
                # The FullLoader parameter handles the conversion from YAML
                # scalar values to Python the dictionary format
                param = yaml.load(file, Loader=yaml.FullLoader)
                param = param.replace('"', '')
                self.__params = [{element.split('=')[0]: element.split('=')[1]}
                                 for element in param.split()]
        except yaml.YAMLError as exc:
            if hasattr(exc, 'problem_mark'):
                mark = exc.problem_mark
                logger.error(f"Error parsing Yaml file {value} "
                             f"at line {(mark.line + 1)}, column {mark.column + 1}")
            else:
                logger.error(self.__msg_error)

            return

    @property
    def development(self):
        return self.__development

    @development.setter
    def development(self, value):
        value = f'{self.okd_path}{value}'
        try:
            with open(value) as file:
                param = yaml.load(file, Loader=yaml.FullLoader)
                for key_1, value in enumerate(param['objects']):
                    metadata = value['metadata']['name']
                    string_data = 'data'
                    if value['kind'] == 'Secret':
                        string_data = 'stringData'

                    data = list(value[string_data].keys())
                    if self.deploy_image[metadata] == data:
                        self.__development.append({
                            metadata: value[string_data]
                        })
                    else:
                        msg = f'development.yml variable: {data} ' \
                            f'is not equal deploy-image.yml variable: ' \
                            f'{self.deploy_image[metadata]}'
                        raise TypeError(msg)

        except yaml.YAMLError as exc:
            if hasattr(exc, 'problem_mark'):
                mark = exc.problem_mark
                logger.error(f"Error parsing Yaml file {value} "
                             f"at line {(mark.line + 1)}, column {mark.column + 1}")
            else:
                logger.error(self.__msg_error)
            return

    @property
    def deploy_image(self):
        return self.__deploy_image

    @deploy_image.setter
    def deploy_image(self, value):
        value = f'{self.okd_path}{value}'
        try:
            with open(value) as file:
                # The FullLoader parameter handles the conversion from YAML
                # scalar values to Python the dictionary format
                config = yaml.load(file, Loader=yaml.FullLoader)

                deployment = [element for element in config['objects']
                              if element['kind'] == 'DeploymentConfig']
                deployment = deployment[0]['spec']['template']['spec']['containers'][0]['env']

                for key, element in enumerate(deployment):
                    config_map = 'secretKeyRef'
                    if 'configMapKeyRef' in element['valueFrom']:
                        config_map = 'configMapKeyRef'

                    name_value = element['valueFrom'][config_map]['name'] \
                        .replace('${', '').replace('}', '')
                    param = [param for param in self.params
                             if list(param.keys())[0] == name_value]
                    if len(param) >= 1:
                        element['valueFrom'][config_map]['name'] = name_value
                        if param[0][name_value] in self.__deploy_image:
                            self.__deploy_image[param[0][name_value]].append(
                                element['valueFrom'][config_map]['key']
                            )
                        else:
                            self.__deploy_image[param[0][name_value]] = [
                                element['valueFrom'][config_map]['key']]

        except yaml.YAMLError as exc:
            if hasattr(exc, 'problem_mark'):
                mark = exc.problem_mark
                logger.error(f"Error parsing Yaml file {value} "
                             f"at line {(mark.line + 1)}, column {mark.column + 1}")
            else:
                logger.error(self.__msg_error)
            return

    def create_env(self):
        pprint(self.development)
        fic = open(".env", "w+")
        for index, element in enumerate(self.development):

            if isinstance(element, (dict,)):
                for key, value in element.items():
                    for key_1, val in value.items():
                        line = f'export {key_1} = {val}'
                        fic.write(line)
                        fic.write('\n')
        fic.close()


test = CheckYml()
