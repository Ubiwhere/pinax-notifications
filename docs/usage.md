# Usage

Integrating notification support into your app is a simple three-step process:

#. create your notice types
#. create your notice templates
#. send notifications


## Creating Notice Types

You need to call `NoticeType.create(label, display, description)` once to
create the notice types for your application in the database where `label` is
just the internal shortname that will be used for the type, `display` is what
the user will see as the name of the notification type and `description` is a
short description.

For example::

    from pinax.notifications.models import NoticeType
    
    NoticeType.create(
        "friends_invite",
        "Invitation Received",
        "you have received an invitation"
    )

Before Django-1.7, the typical way to automatically do this notice type creation
was in a `management.py` file for your app, attached to the syncdb signal.

Django-1.7 deprecated the `post_syncdb` signal, so this system needs to be changed. One possible way to do it is using a custom `AppConfig`.

Here is an example:

    # myapp/signals/handlers.py
    from django.conf import settings
    from django.utils.translation import ugettext_noop as _
    
    def create_notice_types(sender, **kwargs): 
        if "pinax.notifications" in settings.INSTALLED_APPS:
            from pinax.notifications.models import NoticeType
       	    print "Creating notices for myapp" 
            NoticeType.create("friends_invite", _("Invitation Received"), _("you have received an invitation"))
            NoticeType.create("friends_accept", _("Acceptance Received"), _("an invitation you sent has been accepted"))
        else:
            print "Skipping creation of NoticeTypes as notification app not found"

Notice that the code is wrapped in a conditional clause so if
`pinax-notifications` is not installed, your app will proceed anyway.

Note that the display and description arguments are marked for translation by
using ugettext_noop. That will enable you to use Django's makemessages
management command and use `pinax-notifications` i18n capabilities.

    # myapp/apps.py
    from django.apps import AppConfig
    from django.db.models.signals import post_migrate

    from myapp.signals import handlers

    class MyAppConfig(AppConfig):
        name = 'myapp'
        verbose_name = 'My App'
    
        def ready(self):
            post_migrate.connect(handlers.create_notice_types, sender=self)

This will call the handler to create notices after the application is migrated.

    # myapp/__init__.py
    default_app_config = 'myapp.apps.MyAppConfig'

## Notification Templates

### `pinax/notifications/notice_settings.html`

This is a template that ships with `pinax-notifications` and provides an
interview for the user setting of notices that they want to recieve. It is
rendered by the sole view in `pinax.notifications.views` with the context that
is a list of available `notice_types` as well as the `request.user`'s settings
for those notice types.

### Backends

Each backend will have it's own requirements in terms of template(s) it needs
as well as the context it provides in rendering them. It is possible that some
backends may not even use templates.

There are two templates that ship with `pinax-notifications` in support of the
single email backend that is included out of the box:

* ``short.txt`` renders to the email subject
* ``full.txt`` renders to teh email body

In addition to the extra context that is supplied via the `send` call in your
site or app, these templates are rendered with the following context variables:

* `default_http_protocol` - `https` if `settings.PINAX_USE_SSL` is True, otherwise `http`
* `current_site` - `Site.objects.get_current()`
* `base_url` - the default http protocol combined with the current site domain
* `recipient` - the user who is getting the notice
* `sender` - the value supplied to the `sender` kwarg of the `send` method (often this is not set and will be `None`)
* `notice` - display value of the notice type

These two templates that ship with `pinax-notifications` and live at
`pinax/notifications/short.txt` and `pinax/notifications/full.txt` are pretty
vanilla and default. You will likely want to have per notice type
customizations.

In order to do this, each of these templates should be put in a directory on
the template path called `pinax/notifications/<notice_type_label>/<template_name>`.

If any of these are missing, a default would be used.

To use the HTML email backend make sure you have the template with the appropriate HTML in pinax/notifications/<notice_type_label>/templated_email/base.email

You also need to have django-templated-emails installed as a dependency and set

```
PINAX_NOTIFICATIONS_BACKENDS = [("email", "pinax.notifications.backends.email.HtmlEmailBackend"),]
```

in your settings file.


## Sending Notifications

There are two different ways of sending out notifications. We have support
for blocking and non-blocking methods of sending notifications. The most
simple way to send out a notification, for example::

    send([to_user], "friends_invite", {"from_user": from_user})

One thing to note is that `send` is a proxy around either `send_now` or
`queue`. They all have the same signature::

    send(users, label, extra_context)

The parameters are:

* `users` is an iterable of `User` objects to send the notification to.
* `label` is the label you used in the previous step to identify the notice type.
* `extra_content` is a dictionary to add custom context entries to the template
   used to render to notification. This is optional.


### `send_now` vs. `queue` vs. `send`

Lets first break down what each does.

#### `send_now`

This is a blocking call that will check each user for elgibility of the
notice and actually peform the send.

#### `queue`

This is a non-blocking call that will queue the call to `send_now` to
be executed at a later time. To later execute the call you need to use
the `emit_notices` management command.


#### `send`

A proxy around `send_now` and `queue`. It gets its behavior from a global
setting named `PINAX_NOTIFICATIONS_QUEUE_ALL`. By default it is `False`. This
setting is meant to help control whether you want to queue any call to `send`.

`send` also accepts `now` and `queue` keyword arguments. By default each option
is set to `False` to honor the global setting which is `False`. This enables
you to override on a per call basis whether it should call `send_now` or
`queue`.


## Optional Notification Support

In case you want to use `pinax-notification` in your reusable app, you can wrap
the import of `pinax-notification` in a conditional clause that tests if it's
installed before sending a notice. As a result your app or project still
functions without notification.

For example:

    from django.conf import settings

    if "notification" in settings.INSTALLED_APPS:
        from pinax.notifications import models as notification
    else:
        notification = None

and then, later:

    if notification:
        notification.send([to_user], "friends_invite", {"from_user": from_user})
