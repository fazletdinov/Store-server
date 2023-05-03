import stripe
from http import HTTPStatus

from django.views.generic import CreateView, TemplateView
from django.urls import reverse_lazy, reverse
from django.conf import settings
from django.shortcuts import redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from core.mixins.mixin import TitleMixin
from orders.forms import OrderForm
from orders.models import Order
from products.models import Basket

stripe.api_key = settings.STRIPE_SECRET_KEY
DOMAIN = settings.DOMAIN_NAME
endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

class SuccessTemplateView(TitleMixin, TemplateView):
    title = 'Спасибо за заказ!'
    template_name = 'orders/success.html'


class CancelTemplateView(TemplateView):
    template_name = 'orders/cancel.html'


class OderCreateView(TitleMixin, CreateView):
    model = Order
    title = 'Store - Оформление заказа'
    form_class = OrderForm
    template_name = 'orders/order-create.html'
    success_url = reverse_lazy('orders:order_create')

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        baskets = Basket.objects.filter(user=request.user)
        checkout_session = stripe.checkout.Session.create(
            line_items=baskets.stripe_products(),
            metadata={'order_id': self.object.id},
            mode='payment',
            success_url='{}{}'.format(DOMAIN, reverse('orders:order_success')),
            cancel_url='{}{}'.format(DOMAIN, reverse('orders:order_cancel')),
        )
        return redirect(checkout_session.url, status=HTTPStatus.SEE_OTHER)

    def form_valid(self, form):
        form.instance.initiator = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['baskets'] = Basket.objects.filter(user=user)
        return context

@csrf_exempt
def stripe_webhook_view(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        # Retrieve the session. If you require line items in the response, you may include them by expanding line_items.
        session = stripe.checkout.Session.retrieve(
            event['data']['object']['id'],
            expand=['line_items'],
        )

        line_items = session.line_items
        # Fulfill the purchase...
        fulfill_order(line_items)

    # Passed signature verification
    return HttpResponse(status=200)


def fulfill_order(line_items):
    # TODO: fill me in
    print("Fulfilling order")