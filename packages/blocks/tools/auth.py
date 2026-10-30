"""Login, Signup and OTP blocks (ports of shadcn login-01..05, signup-01..05, otp-01..05)."""
from common import page, register, logo, brand_button, LOGO_CSS, LEGAL, LEGAL_CSS

PH = "assets/placeholder.svg"

BASE_CSS = """
  body { background: var(--background); }
  .block-muted { background: var(--muted); }
  .block-narrow { max-inline-size: 24rem; }
  .block-wide { max-inline-size: 56rem; }
  .block-title { margin: 0; font-size: 1.5rem; font-weight: 700; text-wrap: balance; }
  .block-title[data-size='xl'] { font-size: 1.25rem; }
  .block-lead { margin: 0; color: var(--muted-foreground); font-size: 0.875rem; text-wrap: balance; }
  .block-head { display: flex; flex-direction: column; align-items: center; gap: 0.25rem; text-align: center; }
  .block-center { text-align: center; }
  .block-link { margin-inline-start: auto; font-size: 0.875rem; color: inherit; text-underline-offset: 4px; text-decoration: none; }
  .block-link:hover { text-decoration: underline; }
  .field > p.block-center a, .block-foot a { color: inherit; text-decoration: underline; text-underline-offset: 4px; }
  .block-foot { margin: 0; text-align: center; font-size: 0.875rem; color: var(--muted-foreground); }
  .block-label-row { display: flex; align-items: center; }
  .block-image { position: relative; background: var(--muted); min-block-size: 0; }
  .block-image > img { position: absolute; inset: 0; inline-size: 100%; block-size: 100%; object-fit: cover; }
  html.dark .block-image > img { filter: brightness(0.2) grayscale(1); }
  .block-socials { display: grid; gap: 1rem; grid-template-columns: repeat(var(--cols, 3), minmax(0, 1fr)); }
  .block-socials > .btn { inline-size: 100%; }
  .card > .field-separator > span, .card .field-separator > span { background: var(--card); }
""" + LOGO_CSS + LEGAL_CSS


def field(label, type_, id_, placeholder=None, extra="", aside=None, hint=None):
    ph = f' placeholder="{placeholder}"' if placeholder else ""
    head = f'<label for="{id_}">{label}</label>'
    if aside:
        head = f'<div class="block-label-row"><label for="{id_}">{label}</label>{aside}</div>'
    h = f"\n    <p>{hint}</p>" if hint else ""
    return f"""<div role="group" class="field">
    {head}
    <input id="{id_}" type="{type_}"{ph} required{extra}>{h}
  </div>"""


FORGOT = '<a href="#" class="block-link">Forgot your password?</a>'
SEP = lambda text, card=False: f'<div class="field-separator"><hr role="separator"><span>{text}</span></div>'


def login_fields(prefix=""):
    return field("Email", "email", f"{prefix}email", "m@example.com") + "\n  " + field("Password", "password", f"{prefix}password", aside=FORGOT)


blocks = []

# ---------------------------------------------------------------- login
page("login-01", "Login 01", f"""
<main class="cover" data-pad="lg">
  <div class="card block-narrow">
    <header>
      <h2>Login to your account</h2>
      <p>Enter your email below to login to your account</p>
    </header>
    <section>
      <form class="fieldset" onsubmit="event.preventDefault()">
        {login_fields()}
        <div role="group" class="field">
          <button type="submit" class="btn">Login</button>
          <button type="button" class="btn" data-variant="outline">Login with Google</button>
          <p class="block-center">Don't have an account? <a href="#">Sign up</a></p>
        </div>
      </form>
    </section>
  </div>
</main>
""", BASE_CSS)
blocks.append({"id": "login-01", "title": "Login 01", "description": "A simple login form.", "category": "login"})

page("login-02", "Login 02", f"""
<div class="switcher block-split" style="--threshold: 64rem">
  <div class="stack block-pane" data-gap="4">
    <div class="block-brand">{logo()}</div>
    <div class="block-pane-body">
      <form class="fieldset block-narrow" onsubmit="event.preventDefault()">
        <div class="block-head">
          <h1 class="block-title">Login to your account</h1>
          <p class="block-lead">Enter your email below to login to your account</p>
        </div>
        {login_fields()}
        <div role="group" class="field"><button type="submit" class="btn">Login</button></div>
        {SEP("Or continue with")}
        <div role="group" class="field">
          {brand_button("github", "Login with GitHub")}
          <p class="block-center">Don't have an account? <a href="#">Sign up</a></p>
        </div>
      </form>
    </div>
  </div>
  <div class="block-image block-hide-narrow"><img src="{PH}" alt=""></div>
</div>
""", BASE_CSS + """
  .block-split { min-block-size: 100svh; }
  .block-pane { padding: 1.5rem; }
  .block-pane-body { flex: 1; display: flex; align-items: center; justify-content: center; }
  .block-pane-body > form { inline-size: 100%; }
  .block-brand { display: flex; justify-content: center; }
  @media (width >= 48rem) { .block-pane { padding: 2.5rem; } .block-brand { justify-content: flex-start; } }
  @media (width < 64rem) { .block-hide-narrow { display: none; } }
""")
blocks.append({"id": "login-02", "title": "Login 02", "description": "A two column login page with a cover image.", "category": "login"})

page("login-03", "Login 03", f"""
<main class="cover block-muted" data-pad="lg">
  <div class="stack block-narrow" data-gap="6">
    <div class="block-brand">{logo()}</div>
    <div class="card">
      <header class="block-center">
        <h2 class="block-title" data-size="xl">Welcome back</h2>
        <p>Login with your Apple or Google account</p>
      </header>
      <section>
        <form class="fieldset" onsubmit="event.preventDefault()">
          <div role="group" class="field">
            {brand_button("apple", "Login with Apple")}
            {brand_button("google", "Login with Google")}
          </div>
          {SEP("Or continue with")}
          {login_fields()}
          <div role="group" class="field">
            <button type="submit" class="btn">Login</button>
            <p class="block-center">Don't have an account? <a href="#">Sign up</a></p>
          </div>
        </form>
      </section>
    </div>
    {LEGAL}
  </div>
</main>
""", BASE_CSS + "\n  .block-brand { display: flex; justify-content: center; }\n  .card > header.block-center { text-align: center; }")
blocks.append({"id": "login-03", "title": "Login 03", "description": "A login page with a muted background color.", "category": "login"})

page("login-04", "Login 04", f"""
<main class="cover block-muted" data-pad="lg">
  <div class="stack block-wide" data-gap="6">
    <div class="card block-card-split">
      <div class="switcher" data-gap="0" style="--threshold: 44rem">
        <form class="fieldset block-card-form" onsubmit="event.preventDefault()">
          <div class="block-head">
            <h1 class="block-title">Welcome back</h1>
            <p class="block-lead">Login to your Acme Inc account</p>
          </div>
          {login_fields()}
          <div role="group" class="field"><button type="submit" class="btn">Login</button></div>
          {SEP("Or continue with")}
          <div class="block-socials">
            {brand_button("apple", "Login with Apple", True)}
            {brand_button("google", "Login with Google", True)}
            {brand_button("meta", "Login with Meta", True)}
          </div>
          <p class="block-foot">Don't have an account? <a href="#">Sign up</a></p>
        </form>
        <div class="block-image block-hide-narrow"><img src="{PH}" alt=""></div>
      </div>
    </div>
    {LEGAL}
  </div>
</main>
""", BASE_CSS + """
  .block-card-split { padding: 0; }
  .block-card-form { padding: 1.5rem; }
  @media (width >= 48rem) { .block-card-form { padding: 2rem; } }
  @media (width < 48rem) { .block-hide-narrow { display: none; } }
""")
blocks.append({"id": "login-04", "title": "Login 04", "description": "A login page with form and image.", "category": "login"})

page("login-05", "Login 05", f"""
<main class="cover" data-pad="lg">
  <div class="stack block-narrow" data-gap="6">
    <form class="fieldset" onsubmit="event.preventDefault()">
      <div class="block-head">
        <a href="#" class="block-logo"><span class="block-logo-mark block-logo-lg">{logo().split('block-logo-mark">')[1].split('</span>')[0]}</span><span class="sr-only">Acme Inc.</span></a>
        <h1 class="block-title" data-size="xl">Welcome to Acme Inc.</h1>
        <p class="block-lead">Don't have an account? <a href="#">Sign up</a></p>
      </div>
      {field("Email", "email", "email", "m@example.com")}
      <div role="group" class="field"><button type="submit" class="btn">Login</button></div>
      {SEP("Or")}
      <div class="block-socials" style="--cols: 2">
        {brand_button("apple", "Continue with Apple")}
        {brand_button("google", "Continue with Google")}
      </div>
    </form>
    {LEGAL}
  </div>
</main>
""", BASE_CSS + """
  .block-logo-lg { inline-size: 2rem; block-size: 2rem; }
  .block-logo-lg svg { inline-size: 1.5rem; block-size: 1.5rem; }
  .block-lead a { color: inherit; text-decoration: underline; text-underline-offset: 4px; }
  @media (width < 40rem) { .block-socials { --cols: 1 !important; } }
""")
blocks.append({"id": "login-05", "title": "Login 05", "description": "A simple email-only login page.", "category": "login"})

# ---------------------------------------------------------------- signup
def signup_core(prefix="", name=True, pw_grid=False):
    out = []
    if name:
        out.append(field("Full Name", "text", f"{prefix}name", "John Doe"))
    out.append(field("Email", "email", f"{prefix}email", "m@example.com", hint="We'll use this to contact you. We will not share your email with anyone else."))
    if pw_grid:
        out.append(f"""<div role="group" class="field">
    <div class="block-pw-grid">
      <div role="group" class="field"><label for="{prefix}password">Password</label><input id="{prefix}password" type="password" required></div>
      <div role="group" class="field"><label for="{prefix}confirm">Confirm Password</label><input id="{prefix}confirm" type="password" required></div>
    </div>
    <p>Must be at least 8 characters long.</p>
  </div>""")
    else:
        out.append(field("Password", "password", f"{prefix}password", hint="Must be at least 8 characters long."))
        out.append(field("Confirm Password", "password", f"{prefix}confirm", hint="Please confirm your password."))
    return "\n  ".join(out)


PW_GRID_CSS = "\n  .block-pw-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 1rem; }"

page("signup-01", "Signup 01", f"""
<main class="cover" data-pad="lg">
  <div class="card block-narrow">
    <header>
      <h2>Create an account</h2>
      <p>Enter your information below to create your account</p>
    </header>
    <section>
      <form class="fieldset" onsubmit="event.preventDefault()">
        {signup_core()}
        <div role="group" class="field">
          <button type="submit" class="btn">Create Account</button>
          <button type="button" class="btn" data-variant="outline">Sign up with Google</button>
          <p class="block-center">Already have an account? <a href="#">Sign in</a></p>
        </div>
      </form>
    </section>
  </div>
</main>
""", BASE_CSS)
blocks.append({"id": "signup-01", "title": "Signup 01", "description": "A simple signup form.", "category": "signup"})

page("signup-02", "Signup 02", f"""
<div class="switcher block-split" style="--threshold: 64rem">
  <div class="stack block-pane" data-gap="4">
    <div class="block-brand">{logo()}</div>
    <div class="block-pane-body">
      <form class="fieldset block-narrow" onsubmit="event.preventDefault()">
        <div class="block-head">
          <h1 class="block-title">Create your account</h1>
          <p class="block-lead">Fill in the form below to create your account</p>
        </div>
        {signup_core()}
        <div role="group" class="field"><button type="submit" class="btn">Create Account</button></div>
        {SEP("Or continue with")}
        <div role="group" class="field">
          {brand_button("github", "Sign up with GitHub")}
          <p class="block-center">Already have an account? <a href="#">Sign in</a></p>
        </div>
      </form>
    </div>
  </div>
  <div class="block-image block-hide-narrow"><img src="{PH}" alt=""></div>
</div>
""", BASE_CSS + """
  .block-split { min-block-size: 100svh; }
  .block-pane { padding: 1.5rem; }
  .block-pane-body { flex: 1; display: flex; align-items: center; justify-content: center; }
  .block-pane-body > form { inline-size: 100%; }
  .block-brand { display: flex; justify-content: center; }
  @media (width >= 48rem) { .block-pane { padding: 2.5rem; } .block-brand { justify-content: flex-start; } }
  @media (width < 64rem) { .block-hide-narrow { display: none; } }
""")
blocks.append({"id": "signup-02", "title": "Signup 02", "description": "A two column signup page with a cover image.", "category": "signup"})

page("signup-03", "Signup 03", f"""
<main class="cover block-muted" data-pad="lg">
  <div class="stack block-narrow" data-gap="6">
    <div class="block-brand">{logo()}</div>
    <div class="card">
      <header class="block-center">
        <h2 class="block-title" data-size="xl">Create your account</h2>
        <p>Enter your email below to create your account</p>
      </header>
      <section>
        <form class="fieldset" onsubmit="event.preventDefault()">
          {signup_core(pw_grid=True)}
          <div role="group" class="field">
            <button type="submit" class="btn">Create Account</button>
            <p class="block-center">Already have an account? <a href="#">Sign in</a></p>
          </div>
        </form>
      </section>
    </div>
    {LEGAL}
  </div>
</main>
""", BASE_CSS + PW_GRID_CSS + "\n  .block-brand { display: flex; justify-content: center; }\n  .card > header.block-center { text-align: center; }")
blocks.append({"id": "signup-03", "title": "Signup 03", "description": "A signup page with a muted background color.", "category": "signup"})

page("signup-04", "Signup 04", f"""
<main class="cover block-muted" data-pad="lg">
  <div class="stack block-wide" data-gap="6">
    <div class="card block-card-split">
      <div class="switcher" data-gap="0" style="--threshold: 44rem">
        <form class="fieldset block-card-form" onsubmit="event.preventDefault()">
          <div class="block-head">
            <h1 class="block-title">Create your account</h1>
            <p class="block-lead">Enter your email below to create your account</p>
          </div>
          {signup_core(name=False, pw_grid=True)}
          <div role="group" class="field"><button type="submit" class="btn">Create Account</button></div>
          {SEP("Or continue with")}
          <div class="block-socials">
            {brand_button("apple", "Sign up with Apple", True)}
            {brand_button("google", "Sign up with Google", True)}
            {brand_button("meta", "Sign up with Meta", True)}
          </div>
          <p class="block-foot">Already have an account? <a href="#">Sign in</a></p>
        </form>
        <div class="block-image block-hide-narrow"><img src="{PH}" alt=""></div>
      </div>
    </div>
    {LEGAL}
  </div>
</main>
""", BASE_CSS + PW_GRID_CSS + """
  .block-card-split { padding: 0; }
  .block-card-form { padding: 1.5rem; }
  @media (width >= 48rem) { .block-card-form { padding: 2rem; } }
  @media (width < 48rem) { .block-hide-narrow { display: none; } }
""")
blocks.append({"id": "signup-04", "title": "Signup 04", "description": "A signup page with form and image.", "category": "signup"})

LOGO_LG = '<a href="#" class="block-logo"><span class="block-logo-mark block-logo-lg"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg></span><span class="sr-only">Acme Inc.</span></a>'
SIMPLE_CSS = BASE_CSS + """
  .block-logo-lg { inline-size: 2rem; block-size: 2rem; }
  .block-logo-lg svg { inline-size: 1.5rem; block-size: 1.5rem; }
  .block-lead a { color: inherit; text-decoration: underline; text-underline-offset: 4px; }
  @media (width < 40rem) { .block-socials { --cols: 1 !important; } }
"""

page("signup-05", "Signup 05", f"""
<main class="cover" data-pad="lg">
  <div class="stack block-narrow" data-gap="6">
    <form class="fieldset" onsubmit="event.preventDefault()">
      <div class="block-head">
        {LOGO_LG}
        <h1 class="block-title" data-size="xl">Welcome to Acme Inc.</h1>
        <p class="block-lead">Already have an account? <a href="#">Sign in</a></p>
      </div>
      {field("Email", "email", "email", "m@example.com")}
      <div role="group" class="field"><button type="submit" class="btn">Create Account</button></div>
      {SEP("Or")}
      <div class="block-socials" style="--cols: 2">
        {brand_button("apple", "Continue with Apple")}
        {brand_button("google", "Continue with Google")}
      </div>
    </form>
    {LEGAL}
  </div>
</main>
""", SIMPLE_CSS)
blocks.append({"id": "signup-05", "title": "Signup 05", "description": "A simple email-only signup page.", "category": "signup"})

# ---------------------------------------------------------------- otp
def otp_form(card=True, prefix="otp"):
    inner = f"""<form class="fieldset" onsubmit="event.preventDefault()">
        <div role="group" class="field">
          <label for="{prefix}" class="sr-only">Verification code</label>
          <div class="input-otp block-otp" data-length="6">
            <input id="{prefix}" inputmode="numeric" autocomplete="one-time-code" maxlength="6" pattern="[0-9]{{6}}" required>
          </div>
          <p class="block-center">Didn't receive the code? <a href="#">Resend</a></p>
        </div>
        <div role="group" class="field"><button type="submit" class="btn">Verify</button></div>
      </form>"""
    if not card:
        return inner
    return f"""<div class="card">
      <header class="block-center">
        <h2 class="block-title" data-size="xl">Enter verification code</h2>
        <p>We sent a 6-digit code to your email.</p>
      </header>
      <section>
      {inner}
      </section>
    </div>"""


OTP_CSS = """
  .block-otp { --slot: 2.75rem; align-self: center; inline-size: calc(var(--slot) * var(--length)); font-size: 1.25rem; }
  .card > header.block-center { text-align: center; }
  .block-brand { display: flex; justify-content: center; }
"""

page("otp-01", "OTP 01", f"""
<main class="cover" data-pad="lg">
  <div class="block-otp-col">
    {otp_form()}
  </div>
</main>
""", BASE_CSS + OTP_CSS + "\n  .block-otp-col { max-inline-size: 20rem; }")
blocks.append({"id": "otp-01", "title": "OTP 01", "description": "A simple OTP verification form.", "category": "otp"})

page("otp-02", "OTP 02", f"""
<div class="switcher block-split" style="--threshold: 64rem">
  <div class="stack block-pane" data-gap="4">
    <div class="block-brand-start">{logo()}</div>
    <div class="block-pane-body">
      <div class="stack block-otp-col" data-gap="6">
        <div class="block-head">
          <h1 class="block-title">Enter verification code</h1>
          <p class="block-lead">We sent a 6-digit code to your email.</p>
        </div>
        {otp_form(card=False)}
      </div>
    </div>
  </div>
  <div class="block-image block-hide-narrow"><img src="{PH}" alt=""></div>
</div>
""", BASE_CSS + OTP_CSS + """
  .block-otp-col { inline-size: 100%; max-inline-size: 20rem; }
  .block-split { min-block-size: 100svh; }
  .block-pane { padding: 1.5rem; }
  .block-pane-body { flex: 1; display: flex; align-items: center; justify-content: center; }
  .block-brand-start { display: flex; justify-content: center; }
  @media (width >= 48rem) { .block-pane { padding: 2.5rem; } .block-brand-start { justify-content: flex-start; } }
  @media (width < 64rem) { .block-hide-narrow { display: none; } }
""")
blocks.append({"id": "otp-02", "title": "OTP 02", "description": "A two column OTP page with a cover image.", "category": "otp"})

page("otp-03", "OTP 03", f"""
<main class="cover block-muted" data-pad="lg">
  <div class="stack block-narrow" data-gap="6">
    <div class="block-brand">{logo()}</div>
    {otp_form()}
  </div>
</main>
""", BASE_CSS + OTP_CSS)
blocks.append({"id": "otp-03", "title": "OTP 03", "description": "An OTP page with a muted background color.", "category": "otp"})

page("otp-04", "OTP 04", f"""
<main class="cover block-muted" data-pad="lg">
  <div class="stack block-wide" data-gap="6">
    <div class="card block-card-split">
      <div class="switcher" data-gap="0" style="--threshold: 44rem">
        <div class="stack block-card-form" data-gap="6">
          <div class="block-head">
            <h1 class="block-title">Enter verification code</h1>
            <p class="block-lead">We sent a 6-digit code to your email.</p>
          </div>
          {otp_form(card=False)}
        </div>
        <div class="block-image block-hide-narrow"><img src="{PH}" alt=""></div>
      </div>
    </div>
    {LEGAL}
  </div>
</main>
""", BASE_CSS + OTP_CSS + """
  .block-card-split { padding: 0; }
  .block-card-form { padding: 1.5rem; justify-content: center; }
  @media (width >= 48rem) { .block-card-form { padding: 2rem; } }
  @media (width < 48rem) { .block-hide-narrow { display: none; } }
""")
blocks.append({"id": "otp-04", "title": "OTP 04", "description": "An OTP page with form and image.", "category": "otp"})

page("otp-05", "OTP 05", f"""
<main class="cover" data-pad="lg">
  <div class="stack block-narrow" data-gap="6">
    <div class="block-head">
      {LOGO_LG}
      <h1 class="block-title" data-size="xl">Enter verification code</h1>
      <p class="block-lead">We sent a 6-digit code to <strong>m@example.com</strong></p>
    </div>
    {otp_form(card=False)}
    {LEGAL}
  </div>
</main>
""", SIMPLE_CSS + OTP_CSS)
blocks.append({"id": "otp-05", "title": "OTP 05", "description": "A simple centered OTP page.", "category": "otp"})

register(blocks)
print(f"wrote {len(blocks)} auth blocks")
