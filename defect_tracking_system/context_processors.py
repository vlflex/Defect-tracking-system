import config

def website_settings(request):
    """Добавляет настройки сайта в контекст всех шаблонов"""
    return {
        'company_name': config.ServerSetting.COMPANY_NAME,
        'company_website': config.ServerSetting.COMPANY_WEBSITE,
        'site_name': config.WebsiteSettings.SITE_NAME,
        'site_version': config.WebsiteSettings.VERSION,
        'footer_copyright': config.WebsiteSettings.Footer.COPYRIGHT,
        'contact_email': config.WebsiteSettings.Footer.CONTACT_EMAIL,
        'contact_phone': config.WebsiteSettings.Footer.CONTACT_PHONE,
        'navbar_items': {
            'home': config.WebsiteSettings.Navbar.HOME,
            'defects': config.WebsiteSettings.Navbar.DEFECTS,
            'ai': config.WebsiteSettings.Navbar.AI,
            'admin': config.WebsiteSettings.Navbar.ADMIN,
        },
        'ui_config': {
            'primary_color': config.UIConfig.PRIMARY_COLOR,
            'button_radius': config.UIConfig.BUTTON_BORDER_RADIUS,
            'card_radius': config.UIConfig.CARD_BORDER_RADIUS,
        }
    }