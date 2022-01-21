import boto3
from botocore.exceptions import ClientError


def send_email(RECIPIENT, otp):

    # Replace sender@example.com with your "From" address.
    # This address must be verified with Amazon SES.
    SENDER = "Group 6 <gorocal651@icesilo.com>"

    # Specify a configuration set. If you do not want to use a configuration
    # set, comment the following variable, and the
    # ConfigurationSetName=CONFIGURATION_SET argument below.
    # CONFIGURATION_SET = "ConfigSet"

    # If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
    AWS_REGION = "ap-south-1"

    # The subject line for the email.
    SUBJECT = "Varify your email"

    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = (f"Your confirmation code is { otp }")

    # The HTML body of the email.
    BODY_HTML = f"""<p>Welcome! Thanks for signing up.</p>
  <p>Your confirmation code is { otp }</p>
  <br>
  <p>Cheers!</p>
  <p>Team 6, CS559</p>
              """

    # The character encoding for the email.
    CHARSET = "UTF-8"

    # Create a new SES resource and specify a region.
    client = boto3.client('ses', region_name=AWS_REGION)

    
    client.send_email(
        Destination={
            'ToAddresses': [
                RECIPIENT,
            ],
        },
        Message={
            'Body': {
                'Html': {
                    'Charset': CHARSET,
                    'Data': BODY_HTML,
                },
                'Text': {
                    'Charset': CHARSET,
                    'Data': BODY_TEXT,
                },
            },
            'Subject': {
                'Charset': CHARSET,
                'Data': SUBJECT,
            },
        },
        Source=SENDER,
        # If you are not using a configuration set, comment or delete the
        # following line
        # ConfigurationSetName=CONFIGURATION_SET,
    )
    
