from wtforms import Form, validators, PasswordField, StringField, IntegerField, SelectField, TextAreaField

# warning messages for form validation and the required regex for passwords

password_regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_])[A-Za-z\d\W_]{8,}$'
name_message1 = "*Name must be at least 3 characters"
name_message2 = "*Please enter your full name"
user_message = "*Please enter a username"
mail_message = "*Please enter a valid e-mail address"
age_message1 = "*Please enter your age"
age_message2 = "*Age must be at least 18"
pswd_message1 = "*Please set a password"
pswd_message2 = "*Password does not match"
pswd_message3 = "*Password must be a minimum of 8 characters and a maximum of 64 characters"
pswd_message4 = ("*Password must contain at least one lowercase letter, one uppercase letter, one digit, "
                 "and one special character.")


# form classes
class RegisterForm(Form):
    name = StringField("Full name",
                       validators=[validators.length(min=3, message=name_message1),
                                   validators.InputRequired(message=name_message2)])
    username = StringField("Username", validators=[validators.length(min=5, max=35),
                                                   validators.InputRequired(message=user_message)])
    email = StringField("Mail Address", validators=[validators.Email(message=mail_message),
                                                    validators.InputRequired()])
    gender = SelectField("Gender", choices=[("M", "Male"), ("F", "Female"), ("Other", "Other"),
                                            ("Unkown", "I do not want to specify")])
    age = IntegerField("Age", validators=[validators.InputRequired(message=age_message1),
                                          validators.NumberRange(min=18, message=age_message2)])

    password = PasswordField("Password",
                             validators=[validators.InputRequired(message=pswd_message1),
                                         validators.EqualTo(fieldname="confirm", message=pswd_message2),
                                         validators.length(min=8, max=64,
                                                           message=pswd_message3),
                                         validators.Regexp(regex=password_regex,
                                                           message=pswd_message4)]
                             )
    confirm = PasswordField("Re-enter password")


class LoginForm(Form):
    username = StringField("Username")
    password = PasswordField("ciguli")


class CommentForm(Form):
    comment = TextAreaField(validators=[validators.InputRequired(), validators.Length(min=3)])
