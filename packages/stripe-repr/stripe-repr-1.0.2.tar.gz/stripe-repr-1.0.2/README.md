# Stripe Repr

A monkey-patch library to provide more compact representation for Stripe objects.

If you ever tried to explore the Stripe API from the console, you did notice that the representation format of the objects is overly verbose. A single call of something like `stripe.Customer.list()` pollutes the output with hundreds of lines of the output.

To simplify the exploratory work for ourselves, we created a simple `stripe_repr` library that we install in our development environment. Then we use it as-is:

```python
import stripe_repr

stripe_repr.patch()
```

The output becomes more manageable:

```
>>> stripe.Customer.list()
ListObject(data=[Customer(id='cus_HOQHEicZ9WvOJk'), ..., Customer(id='cus_HOG3cB0b8sin1q')])
```

The second annoyance is date-times, represented in seconds since epoch. Whenever possible, the repr tries to convert them to a proper datetime and format as a string. When it's not enough, you can call a method `formatted_dict()` that also has a shortcut `d()`.

```python
In  [1]: stripe.Invoice.retrieve('in_xxxxx).d()
Out [1]:
 {'id': 'in_xxxxx',
 'object': 'invoice',
 'account_country': 'US',
 ...
 'created': '2020-06-02T16:58:18',
 'currency': 'usd',
}
```
