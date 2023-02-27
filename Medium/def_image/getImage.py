cb_security=['cybersecurity','information-security','blockchain','Cryptocurrency','web3','security']
data_science=['ai','ml','deep-learning','nlp','data-science','data-analysis','image-processing']
cloud_comp=['cloud-computing','cloud-services','dev-ops']
app_dev=['android','app-development','flutter']
web_dev=['web-development','Software-Development','front-end-development']

image_src=[{'data-science':'https://d1m75rqqgidzqn.cloudfront.net/wp-data/2019/09/11134058/What-is-data-science-2.jpg'},
           {'cloud-comp':'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRhH4Jd0x2eGLltI4LlNIAD0GgQPnpeHJTvcQ&usqp=CAU'},
            {'app-dev':'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTr5C37y_7CIpkmFSGcEBSLrf0WODe3WvhR4A&usqp=CAU'},
            {'web-dev':'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTpfK84JnyFZ7TEAQvc-cNMD3W4PXuypt6nNQ&usqp=CAU'},
            {'cb-security':'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQZam9qsK_EuHuyP_vHvMpLqkKf6M8MylMlVQ&usqp=CAU'}
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
