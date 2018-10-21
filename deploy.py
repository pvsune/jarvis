#!/usr/bin/env python
import logging
import os

import docker
from kubernetes import client, config


logging.basicConfig(level=logging.INFO)


def build_image(path, image):
    logging.info('Building image "%s"...', image)

    client = docker.from_env()
    image = client.images.build(path=path, tag=image)

    logging.info('Done...')
    return image


def set_image(name, namespace, image):
    logging.info('Setting deployment to "%s"...', image)

    config.load_kube_config()
    c = client.ExtensionsV1beta1Api()
    deployment = c.read_namespaced_deployment(name, namespace)
    deployment.spec.template.spec.containers[0].image = image
    res = c.patch_namespaced_deployment(
        name=name, namespace=namespace, body=deployment
    )

    logging.info('Done...')
    return res


def deploy(name, path, image, namespace='default', env={}):
    # Easier to set dockerpy client via envvar.
    for k, v in env.items():
        os.environ[k] = v
    build_image(path, image)
    set_image(name, namespace, image)


if __name__ == '__main__':
    app_name = ''
    app_path = ''
    app_image_name = ''
    env = {
        'DOCKER_TLS_VERIFY': '',
        'DOCKER_HOST': '',
        'DOCKER_CERT_PATH': '',
        'DOCKER_API_VERSION': '',
    }
    deploy(app_name, app_path, app_image_name, env=env)
