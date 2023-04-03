cb_security=['cybersecurity','information-security','blockchain','Cryptocurrency','web3','security']
data_science=['ai','machine-learning','deep-learning','nlp','data-science','data-analysis','image-processing']
cloud_comp=['cloud-computing','cloud-services','dev-ops']
app_dev=['android','app-development','flutter']
web_dev=['web-development','software-development','backend-development','backend']

image_src=[{'data-science':'https://miro.medium.com/v2/resize:fill:140:140/1*bkgZjtPIr4lGPHIN0S6ETg.jpeg'},
           {'cloud-comp':'https://miro.medium.com/v2/resize:fill:140:140/1*EZScbwq2J7pbB6oR4kM8kA.jpeg'},
            {'app-dev':'https://miro.medium.com/v2/resize:fill:140:140/1*URM9DzJ0YB4mYWv1k61doA.jpeg'},
            {'web-dev':'https://miro.medium.com/v2/resize:fill:140:140/1*uZxTT58Z7nuOLjWn2EeUhQ.jpeg'},
            {'cb-security':'https://miro.medium.com/v2/resize:fill:140:140/0*WQ3LjCh_3LN0D3m5'}
           ]

def get_image(tag:str):
    if tag in data_science:
        return image_src[0]['data-science']
    elif tag in cloud_comp:
        return image_src[1]['cloud-comp']
    elif tag in app_dev:
        return image_src[2]['app-dev']
    elif tag in web_dev:
        return image_src[3]['web-dev']
    elif tag in cb_security:
        return image_src[4]['cb-security']
