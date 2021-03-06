from kubernetes import client, config


def create_deployment_object(images, tags, rc, envs, name):
    image = images + ':' + tags

    container = client.V1Container(
        name=name,
        image='hub.cbble.com/' + image,
        env=[{'name': 'CONFIG_ENV', 'value': envs}],
        # args=["sleep", "600000"],
        resources=client.V1ResourceRequirements(requests={'cpu': '1000m', 'memory': '1024M'},
                                                limits={'cpu': '1500m', 'memory': '2048M'})
    )

    template = client.V1PodTemplateSpec(
        metadata=client.V1ObjectMeta(labels={"app": name}),
        spec=client.V1PodSpec(containers=[container],
                              image_pull_secrets=[{'name': 'regsecret'}]
                              ))
    # 指定 specific
    spec = client.ExtensionsV1beta1DeploymentSpec(
        replicas=rc,
        template=template)
    # Instantiate the deployment object

    deployment = client.ExtensionsV1beta1Deployment(
        api_version="extensions/v1beta1",
        kind="Deployment",
        metadata=client.V1ObjectMeta(name=name),
        spec=spec)

    return deployment


def create_deployment(api_instance, deployment, ns):
    api_response = api_instance.create_namespaced_deployment(
        body=deployment,
        namespace=ns)
    print("Deployment created. status='%s'" % str(api_response.status))
    return api_response.status


def update_deployment(api_instance, images, tags, ns, rc, envs):
    # Update container image
    #  = deployment = client.ExtensionsV1beta1Deployment()
    deployment = client.ExtensionsV1beta1Deployment(
        api_version="extensions/v1beta1",
        kind="Deployment",
        metadata=client.V1ObjectMeta(name='hsdgold-console-pc'))
    if '/' in images:
        name = images.split('/')[-1]
    else:
        name = images
    images = 'hub.heshidai.com/' + images + ':' + tags
    print(images)
    deployment.spec.template.spec.containers[0].image = images
    deployment.spec.replicas = rc
    deployment.spec.template.spec.containers[0].env[0]['value'] = envs
    # Update the deployment
    api_response = api_instance.patch_namespaced_deployment(
        name=name,
        namespace=ns,
        body=deployment)
    print("Deployment updated. status='%s'" % str(api_response.status))


def delete_deployment(api_instance, ns, images):
    # Delete deployment
    if '/' in images:
        name = images.split('/')[-1]
    else:
        name = images

    api_response = api_instance.delete_namespaced_deployment(
        name=name,
        namespace=ns,
        body=client.V1DeleteOptions(
            propagation_policy='Foreground',
            grace_period_seconds=5))
    # print("Deployment deleted. status='%s'" % str(api_response.status))
    return api_response.status


def main():
    config.load_kube_config()

    extensions_v1beta1 = client.ExtensionsV1beta1Api()

    # ns = u'bb'.encode('utf-8')
    # msg = u'base/nginx'.encode('utf-8')
    # tags = u'1.7.9'.encode('utf-8')
    # rc = int(u'1'.encode('utf-8'))
    # env = u'test'.encode('utf-8')

    # deployment = create_deployment_object(tags=tags, images=msg, envs=env, rc=rc)

    # create_deployment(extensions_v1beta1, deployment, ns)
    dp_name = 'goodthis'
    ns = 'default'
    msg = 'base/nginx'
    tags = 'latest'
    rc = 1
    env = 'nnnnn'
    dp = client.ExtensionsV1beta1Api()
    # a = dp.read_namespaced_deployment(name='2048', namespace='ba')
    # update_deployment(extensions_v1beta1, msg, tags, ns, rc, env)
    # deployment = client.ExtensionsV1beta1Deployment(
    #     api_version="extensions/v1beta1",
    #     kind="Deployment",
    #     metadata=client.V1ObjectMeta(name=name),
    #     spec=spec)
    deployment = create_deployment_object(tags=tags, images=msg, rc=rc, envs=env, name=dp_name)
    create_deployment(extensions_v1beta1, deployment, ns)

    # delete_deployment(extensions_v1beta1, ns=ns, images=msg)


if __name__ == '__main__':
    main()
