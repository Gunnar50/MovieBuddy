# Allow CSRF token to be used in API calls from Javascript
CSRF_COOKIE_HTTPONLY = False

SELF = "'self'"
UNSAFE_INLINE = "'unsafe-inline'"

# Copied from Flask-Talisman GOOGLE_CSP_POLICY
CSP_POLICY = {
    'default-src': [SELF],
    'connect-src': [
        SELF,
        "https://www.gstatic.com/glue/cookienotificationbar/",
    ],
    'img-src': [SELF, 'https://lh3.googleusercontent.com/'],
    'frame-src': [
        SELF,
        'accounts.google.com',
    ],
    'font-src': [
        SELF,
        'themes.googleusercontent.com',
        'data:',
        'https://fonts.gstatic.com/s/',
    ],
    'media-src': ['https://kstatic.googleusercontent.com/files/'],
    'script-src': [
        SELF,
        'ajax.googleapis.com',
        'http://www.googletagmanager.com',
        "https://www.gstatic.com/brandstudio/kato/",
        "https://www.gstatic.com/glue/cookienotificationbar/",
    ],
    'style-src': [
        SELF,
        'ajax.googleapis.com',
        'fonts.googleapis.com',
        "https://www.gstatic.com/glue/cookienotificationbar/",
        'accounts.google.com',
    ],
}

# GA4 / GTM
# Google domains taken from https://www.google.com/supported_domains
GOOGLE_TLDs = ('com', 'ad', 'ae', 'af', 'ag', 'al', 'am', 'ao', 'ar', 'as',
               'at', 'au', 'az', 'ba', 'bd', 'be', 'bf', 'bg', 'bh', 'bi', 'bj',
               'bn', 'bo', 'br', 'bs', 'bt', 'bw', 'by', 'bz', 'ca', 'cd', 'cf',
               'cg', 'ch', 'ci', 'ck', 'cl', 'cm', 'cn', 'co', 'cr', 'cu', 'cv',
               'cy', 'cz', 'de', 'dj', 'dk', 'dm', 'do', 'dz', 'ec', 'ee', 'eg',
               'es', 'et', 'fi', 'fj', 'fm', 'fr', 'ga', 'ge', 'gg', 'gh', 'gi',
               'gl', 'gm', 'gr', 'gt', 'gy', 'hk', 'hn', 'hr', 'ht', 'hu', 'id',
               'ie', 'il', 'im', 'in', 'iq', 'is', 'it', 'je', 'jm', 'jo', 'jp',
               'ke', 'kh', 'ki', 'kg', 'kr', 'kw', 'kz', 'la', 'lb', 'li', 'lk',
               'ls', 'lt', 'lu', 'lv', 'ly', 'ma', 'md', 'me', 'mg', 'mk', 'ml',
               'mm', 'mn', 'mt', 'mu', 'mv', 'mw', 'mx', 'my', 'mz', 'na', 'ng',
               'ni', 'ne', 'nl', 'no', 'np', 'nr', 'nu', 'nz', 'om', 'pa', 'pe',
               'pg', 'ph', 'pk', 'pl', 'pn', 'pr', 'ps', 'pt', 'py', 'qa', 'ro',
               'ru', 'rw', 'sa', 'sb', 'sc', 'se', 'sg', 'sh', 'si', 'sk', 'sl',
               'sn', 'so', 'sm', 'sr', 'st', 'sv', 'td', 'tg', 'th', 'tj', 'tl',
               'tm', 'tn', 'to', 'tr', 'tt', 'tw', 'tz', 'ua', 'ug', 'uk', 'uy',
               'uz', 'vc', 've', 'vi', 'vn', 'vu', 'ws', 'rs', 'za', 'zm', 'zw',
               'cat')
GOOGLE_DOMAINS = [f'*.google.{tld}' for tld in GOOGLE_TLDs]

CSP_POLICY['connect-src'] += [
    "https://*.gstatic.com",
    "https://*.googleapis.com",
    'https://*.google-analytics.com',
    'https://*.analytics.google.com',
    'https://*.googletagmanager.com',
    'https://*.g.doubleclick.net',
] + GOOGLE_DOMAINS
CSP_POLICY['frame-src'] += ['https://www.googletagmanager.com']
CSP_POLICY['img-src'] += [
    'https://*.google-analytics.com',
    'https://*.analytics.google.com',
    'https://*.googletagmanager.com',
    'https://*.g.doubleclick.net',
] + GOOGLE_DOMAINS
CSP_POLICY['script-src'] += ['https://*.googletagmanager.com']

# Google login
CSP_POLICY['connect-src'] += ['https://accounts.google.com']
CSP_POLICY['script-src'] += ['https://accounts.google.com']
CSP_POLICY['style-src'] += ['https://accounts.google.com']
CSP_POLICY['frame-src'] += ['https://accounts.google.com']
