from flask import Flask, request, render_template
from core import Core
from payment import Payment

application = Flask(__name__)
core = Core()
payment = Payment()

@application.route('/', methods = ['POST', 'GET'])
@application.route('/index', methods = ['POST', 'GET'])
def index():
    publicKey = request.form.get('publicKey')
    privateKey = request.form.get('privateKey')
    validPublicKey = core.checkWallet(publicKey, privateKey)
    if validPublicKey:
        core.createUser(publicKey, privateKey)
        services = core.getServicesWithStates(publicKey)
        return render_template(
            'index.html',
            publicKey = publicKey,
            services = services
        )
    else:
        return render_template(
            'index.html'
        )

@application.route('/subscribe', methods = ['POST'])
def subscribe():
    publicKey = request.form.get('publicKey')
    serviceId = request.form.get('serviceId')
    core.subscribe(publicKey, serviceId)
    services = core.getServicesWithStates(publicKey)
    return render_template(
        'index.html',
        publicKey = publicKey,
        services = services
    )

@application.route('/unsubscribe', methods = ['POST'])
def unsubscribe():
    publicKey = request.form.get('publicKey')
    serviceId = request.form.get('serviceId')
    core.unsubscribe(publicKey, serviceId)
    services = core.getServicesWithStates(publicKey)
    return render_template(
        'index.html',
        publicKey = publicKey,
        services = services
    )

@application.route('/subscribe_all', methods = ['POST'])
def subscribeAll():
    publicKey = request.form.get('publicKey')
    core.subscribeAll(publicKey)
    services = core.getServicesWithStates(publicKey)
    return render_template(
        'index.html',
        publicKey = publicKey,
        services = services
    )

@application.route('/unsubscribe_all', methods = ['POST'])
def unsubscribeAll():
    publicKey = request.form.get('publicKey')
    core.unsubscribeAll(publicKey)
    services = core.getServicesWithStates(publicKey)
    return render_template(
        'index.html',
        publicKey = publicKey,
        services = services
    )

if __name__ == '__main__':
    payment.setDaemon(True)
    payment.start()
    application.debug = True
    application.run()
