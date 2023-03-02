import os
import secrets
from calendar import week
from datetime import timedelta
from itsdangerous import TimedSerializer as Serializer
from flask import render_template, url_for, flash, redirect, session, request
from PIL import Image
from blogwebsite.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm,PostForm
from blogwebsite import app, mysql, bcrypt, User_Token, mail
from flask_mail import Message

conn = mysql.connect()
cursor = conn.cursor()
app.secret_key = "579162fdrfughhxtds4rd886fjur65edfg"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "redis"

posts = [
    {
        "authors": "Horaverse",
        "content_link": "https://medium.com/@horaverse/earn-crypto-every-month-with-crypto-idle-miner-bb828ef0b3f8?source=topics_v2---------0-84--------------------b60474fd_6ab7_42ef_967b_c009f55f9207-------17",
        "title": "Earn Crypto Every Month with Crypto Idle Miner",
        "content": "Hi Crypto Miners, We have a new surprise for you, in addition to our recent releases and updates. This surprise will make our event system even more interesting, fun, and\u2026 profitable! As many of you know, we have special events in Crypto Idle Miner, events that provide exclusive prize pools\u2026",
        "image": "https://miro.medium.com/fit/c/140/140/1*UdrhSE37mkEbImiH3o6O8Q.png",
        "topic": "Cryptocurrency",
        "scrape_time": "2023-02-23 16:43:57.901360"
    },
    {
        "authors": "LayerZero Labs",
        "content_link": "https://medium.com/layerzero-official/public-goods-by-layerzero-9220b9fa3d2d?source=topics_v2---------1-84--------------------b60474fd_6ab7_42ef_967b_c009f55f9207-------17",
        "title": "Public Goods by LayerZero",
        "content": "Testnet Bridge Anyone who has ever spent time developing on Goerli has suffered the same problem: getting any reasonable amount of Goerli-ETH is near impossible. One of our first experiences with testing systems at scale was a battle of \u201cus\u201d against the Goerli faucet. We camped the faucet for days, begged, and\u2026",
        "image": "https://miro.medium.com/fit/c/140/140/1*qxeogOqDoe4TkIkerDuJwA.png",
        "topic": "Cryptocurrency",
        "scrape_time": "2023-02-23 16:43:57.902310"
    },
    {
        "authors": "Henri Stern",
        "content_link": "https://medium.com/privy-io/web3-for-users-not-experts-52c692c25bb1?source=topics_v2---------3-84--------------------b60474fd_6ab7_42ef_967b_c009f55f9207-------17",
        "title": "Web3 for users, not experts.",
        "content": "Introducing embedded wallets Privy is the easiest way for developers to onboard all users to web3, regardless of whether they already have a wallet, across mobile and desktop. Today, we are excited to announce the next step in our product journey: embedded wallets. Embedded wallets make it easy for developers\u2026",
        "image": "https://miro.medium.com/fit/c/140/140/1*Jznj4SRRAT4WWajeh5yatw.jpeg",
        "topic": "Cryptocurrency",
        "scrape_time": "2023-02-23 16:43:57.903308"
    },
    {
        "authors": "Plutus",
        "content_link": "https://medium.com/plutus/important-update-plutusdex-paused-eea-99f8d2747723?source=topics_v2---------4-84--------------------b60474fd_6ab7_42ef_967b_c009f55f9207-------17",
        "title": "Important Update | PlutusDEX Paused (EEA)",
        "content": "Over the last three years, research has shown that Pluton Rewards are the most demanded feature out of Plutus\u2019 product family. \u2026",
        "image": "https://miro.medium.com/fit/c/140/140/0*nKI67b7jBiyXvQpY",
        "topic": "Cryptocurrency",
        "scrape_time": "2023-02-23 16:43:57.903308"
    },
    {
        "authors": "TrueUSD",
        "content_link": "https://medium.com/@trueusd/trueusd-becomes-first-usd-backed-stablecoin-to-secure-minting-with-proof-of-reserves-fe8dbffde44f?source=topics_v2---------5-84--------------------b60474fd_6ab7_42ef_967b_c009f55f9207-------17",
        "title": "TrueUSD Becomes First USD-Backed Stablecoin to Secure Minting with \u2018Proof of Reserves\u2019",
        "content": "Today we are pleased to announce that TrueUSD (TUSD) is now using Chainlink\u2019s Proof of Reserves technology to secure minting and further ensure transparency and reliability. As the first stablecoin to programmatically control minting with real-time on-chain verification of off-chain reserves, TUSD is demonstrating a new paradigm of decentralization, transparency\u2026",
        "image": "https://miro.medium.com/fit/c/140/140/1*qc53ZggkiYRKyFaW5ckmhw@2x.jpeg",
        "topic": "Cryptocurrency",
        "scrape_time": "2023-02-23 16:43:57.904366"
    },
    {
        "authors": "ROFLCOPTER | The Return",
        "content_link": "https://medium.com/@ROFLCOPTERtoken/the-return-of-roflcopter-216029cdc4ee?source=topics_v2---------7-84--------------------b60474fd_6ab7_42ef_967b_c009f55f9207-------17",
        "title": "The return of ROFLCOPTER",
        "content": "The Return of the ROFLCOPTER ROFLCOPTER is back and launched as a cryptocurrency on the Ethereum Blockchain as a meme-utility token. WTFBOMBS and OMG MISSILES will be dropped occasionally from the ROFLCOPTER. Now, you may be asking yourself\u2026 What the FUCK is a WTFBOMB and OMGMISSILES??! WTFBOMBS are major buybacks deployed from the ROFLCOPTER as a buyback every\u2026",
        "image": "https://miro.medium.com/fit/c/140/140/0*CRYbyFhGHfEV-E3t",
        "topic": "Cryptocurrency",
        "scrape_time": "2023-02-23 16:43:57.905309"
    },
    {
        "authors": "BinaryX",
        "content_link": "https://medium.com/@binary-x/what-is-cyberdragon-boss-raid-a-new-gameplay-on-binaryx-fb1abed5e808?source=topics_v2---------8-84--------------------b60474fd_6ab7_42ef_967b_c009f55f9207-------17",
        "title": "What is CyberDragon: Boss Raid?",
        "content": "Boss Raid is an exciting new game set in the world of CyberDragon, where players can come together to battle a powerful boss. The game is designed for players to consume BNX to attack the boss within a specified time, and if successful, the player will receive a battle reward\u2026",
        "image": "https://miro.medium.com/fit/c/140/140/1*yGPJdJzZiiCqmKW8UV9tnw.jpeg",
        "topic": "Cryptocurrency",
        "scrape_time": "2023-02-23 16:43:57.906364"
    },
    {
        "authors": "AlgoGamingGuild",
        "content_link": "https://medium.com/@AlgoGamingGuild/agg-acquires-the-algoseas-nft-marketplace-50153bfda8d8?source=topics_v2---------9-84--------------------b60474fd_6ab7_42ef_967b_c009f55f9207-------17",
        "title": "AGG acquires the AlgoSeas NFT Marketplace",
        "content": "We, at the Algo Gaming Guild, are extremely excited to announce our acquisition of the AlgoSeas NFT marketplace with the intention of integrating it into our upcoming platform, CoolDWN. We have had a close relationship with the AlgoSeas team for quite some time now and this transaction has truly been\u2026",
        "image": "https://miro.medium.com/fit/c/140/140/1*-dJs-vqTE08qtLyvBLNcFg.png",
        "topic": "Cryptocurrency",
        "scrape_time": "2023-02-23 16:43:57.906364"
    },
    {
        "authors": "Dr_jackal",
        "content_link": "https://medium.com/@akabane.kurodo786/tutorial-how-to-install-a-full-node-on-the-sui-network-testnet-wave-3-974cf417550f?source=topics_v2---------10-84--------------------eea93dfd_7a32_440e_a600_74888c377d60-------17",
        "title": "Tutorial \u2014 How to install a Full node on the SUI network \u2014 TESTNET WAVE 3",
        "content": "Video Tutorial \u201cSui of mysten labs\u201d, I don\u2019t know why I love to pronounce it. Today I\u2019m going to do more than just pronounce it, I\u2019m going to give you the opportunity to participate on their testnet. Are you ready? Let\u2019s go! Who am I I am passionate about the world of blockchain\u2026",
        "image": "https://miro.medium.com/fit/c/140/140/1*61FmuGkPGUPpfaaksJjQYQ.png",
        "topic": "Cryptocurrency",
        "scrape_time": "2023-02-23 16:43:57.907306"
    },
    {
        "authors": "We All United",
        "content_link": "https://medium.com/@weallunited2022/introducing-a-new-plan-to-secure-the-future-of-our-token-and-build-more-trust-in-the-community-44397e07fceb?source=topics_v2---------11-84--------------------eea93dfd_7a32_440e_a600_74888c377d60-------17",
        "title": "Introducing a New Plan to Secure The Future of Our Token and Build More Trust in the Community",
        "content": "Introducing a New Plan to Secure The Future of Our Token and Build More Trust in the Community WE ALL UNITED are committed to building a community that trusts us and our vision. To achieve this goal, we have developed a plan that involves asking our top holders to contribute\u2026",
        "image": "https://miro.medium.com/fit/c/140/140/1*SkqAtRd6xsnlL3eDMd-9_A.jpeg",
        "topic": "Cryptocurrency",
        "scrape_time": "2023-02-23 16:43:57.907306"
    },
    {
        "authors": "COTI",
        "content_link": "https://medium.com/@cotinetwork/an-all-time-high-record-for-the-coti-treasury-half-a-billion-coti-has-been-deposited-fdd084efeb1b?source=topics_v2---------12-84--------------------eea93dfd_7a32_440e_a600_74888c377d60-------17",
        "title": "An All-Time High Record For the COTI Treasury: half a Billion $COTI Has Been Deposited!",
        "content": "We are proud to share an amazing milestone for the COTI Treasury: A total balance of over half a billion $COTI has been deposited!",
        "image": "https://miro.medium.com/fit/c/140/140/0*ds2oDMoKGxH6mkhq",
        "topic": "Cryptocurrency",
        "scrape_time": "2023-02-23 16:43:57.908312"
    },
    {
        "authors": "TipLink",
        "content_link": "https://medium.com/@TipLink/tiplink-raises-6m-co-led-by-sequoia-and-multicoin-to-unlock-the-ultimate-distribution-mechanism-b403aa69634f?source=topics_v2---------13-84--------------------eea93dfd_7a32_440e_a600_74888c377d60-------17",
        "title": "TipLink raises $6m, co-led by Sequoia and Multicoin, to unlock the ultimate distribution mechanism to send crypto & NFTs",
        "content": "TLDR: We raised $6m, launched our API to send crypto + NFTs with a link, and we are hiring! We are thrilled to announce that we have raised $6m in seed funding led by Sequoia Capital and Multicoin Capital. TipLink allows users to send crypto or NFTs with just a\u2026",
        "image": "https://miro.medium.com/fit/c/140/140/1*pMCvTmh4AZOyTRwCjIMNiw.png",
        "topic": "Cryptocurrency",
        "scrape_time": "2023-02-23 16:43:57.908312"
    },
    {
        "authors": "Crypto Enthusiast",
        "content_link": "https://medium.com/@cryptoenthusiasts71/uhive-social-network-review-and-token-financial-analysis-f0838d8d854d?source=topics_v2---------14-84--------------------eea93dfd_7a32_440e_a600_74888c377d60-------17",
        "title": "Uhive Social Network Review and Token Financial Analysis",
        "content": "I\u2019m a crypto enthusiast, but am also a realist. While I don\u2019t believe crypto will take over the world anytime soon, the potential for massive growth is there. I don\u2019t think any of us will forget the bull run in December 2017 that brought cryptos to the world stage. But\u2026",
        "image": "https://miro.medium.com/fit/c/140/140/0*j_wokTzx7XCUOoIK",
        "topic": "Cryptocurrency",
        "scrape_time": "2023-02-23 16:43:57.909314"
    },
    {
        "authors": "SOV",
        "content_link": "https://medium.com/@eossov/sov-giveaway-for-sov-invaders-37d5447292fe?source=topics_v2---------15-84--------------------eea93dfd_7a32_440e_a600_74888c377d60-------17",
        "title": "SOV Giveaway for SOV INVADERS!",
        "content": "Here is a chance to earn some SOV for designing promotional material for our upcoming game SOV INVADERS! Prizes will be awarded in \u00a7SOV at a $USDT equivalent (SOVDEX, NEWDEX, DefiBOX avg pricing) when the winners are announced on March 8th 2023. \n1st place = $50 \u2248 \u00a728,000\n2nd place =\u2026",
        "image": "https://miro.medium.com/fit/c/140/140/1*RIRVxBhvJvbYrr5-ihI6fg.png",
        "topic": "Cryptocurrency",
        "scrape_time": "2023-02-23 16:43:57.909314"
    },
    {
        "authors": "Larpseidon",
        "content_link": "https://medium.com/smilee-finance/smilee-trading-competition-80-000-in-rewards-1b099dce8e23?source=topics_v2---------16-84--------------------eea93dfd_7a32_440e_a600_74888c377d60-------17",
        "title": "SMILEE TRADING COMPETITION\u2014$80,000 in Rewards",
        "content": "Smilee is kicking things off with a private testnet trading competition. It doesn\u2019t require real funds to compete, and you\u2019ll get the first exclusive ability to use our products! TL;DR Total rewards pool: $80,000 Win up to: $18,200 Round 1 WL spots: 420 Total duration: 6 weeks Wen: March 1st \u2026",
        "image": "https://miro.medium.com/fit/c/140/140/1*IV6sIslioNdLIJQVzO-5Sg.png",
        "topic": "Cryptocurrency",
        "scrape_time": "2023-02-23 16:43:57.910367"
    },
    {
        "authors": "Anastasia",
        "content_link": "https://medium.com/@mindsetbillionaire83/how-to-make-10-000-every-day-with-chat-gpt-d00ab81a5836?source=topics_v2---------17-84--------------------eea93dfd_7a32_440e_a600_74888c377d60-------17",
        "title": "How To Make $10,000 Every Day With CHAT GPT",
        "content": "Chat GPT, also known as the \u201cGenerative Pre-trained Transformer,\u201d is a potent machine learning model that can produce language that resembles that of a person. The creation of written material for websites or social media postings, which may assist in generating income through advertising or affiliate marketing, is one potential\u2026",
        "image": "https://miro.medium.com/fit/c/140/140/1*jdlj7gMW-MBj8ybiEan9cA.png",
        "topic": "Cryptocurrency",
        "scrape_time": "2023-02-23 16:43:57.910367"
    },
    {
        "authors": "Metaline",
        "content_link": "https://medium.com/@Metaline001/metaline-announces-alchemy-pay-integration-7ccd1896c8d?source=topics_v2---------18-84--------------------eea93dfd_7a32_440e_a600_74888c377d60-------17",
        "title": "MetaLine Announces Alchemy Pay Integration",
        "content": "Dear MetaLine followers, We are happy to announce that we have partnered with Alchemy Pay, and will soon be supporting payments on the MetaLine official website through Alchemy Pay. After integrating with Alchemy Pay, MetaLine will allow end-users to accept fiat and crypto payments on our platform.This integration enables MetaLine\u2026",
        "image": "https://miro.medium.com/fit/c/140/140/1*j8Cm_cAFtkulucGzioXq4Q.png",
        "topic": "Cryptocurrency",
        "scrape_time": "2023-02-23 16:43:57.911309"
    },
    {
        "authors": "Hacken.AI",
        "content_link": "https://medium.com/@hackenclub/hdao-voting-power-influence-and-change-with-hai-410349c39178?source=topics_v2---------19-84--------------------eea93dfd_7a32_440e_a600_74888c377d60-------17",
        "title": "hDAO Voting Power: Influence and Change with HAI",
        "content": "Diversity, Equity, and Inclusion (DEI) have become crucial principles for any organization, and they are especially relevant in the crypto world. Decentralization promises to create a more equitable and accessible financial system, but it must be accompanied by inclusive decision-making processes that reflect the needs and values of diverse stakeholders. \u2026",
        "image": "https://miro.medium.com/fit/c/140/140/1*_ipydcsWmKeb1NC1SEM0uQ.png",
        "topic": "Cryptocurrency",
        "scrape_time": "2023-02-23 16:43:57.911309"
    }
]


@app.route("/")
@app.route("/home")
def home():
    # if session.get("id") is None:
    #     return redirect(url_for("login"))
    return render_template  ('home.html', posts=posts)


@app.route("/about")
def about():
    # if session.get("id") is None:
    #     return redirect(url_for("login"))
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user_query = ''' insert into User_Profile(user_name,user_email,user_pass,user_pic)
                            values(%s,%s,%s,%s)'''
        user_info = (
            form.username.data, form.email.data, bcrypt.generate_password_hash(form.password.data),
            'default_profile_pic.jpg')
        # execute the query
        cursor.execute(user_query, user_info)
        conn.commit()
        flash(f'Your account has been created now you can log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if session.get("id") is not None:
        return redirect(url_for("home"))
    elif form.validate_on_submit():
        cursor.execute(''' SELECT user_id,user_name,user_email,user_password from User_Profile 
                                        where user_email=%s''',
                       [form.email.data])
        user_pass = cursor.fetchone()

        if user_pass is None:
            flash("User doesn't exist please register yourself first !!", 'danger')
            return redirect(url_for('register'))
        elif user_pass and bcrypt.check_password_hash(user_pass[3], form.password.data):
            if form.remember.data is True:
                app.config["SESSION_PERMANENT"] = True
            else:
                app.permanent_session_lifetime = timedelta(weeks=5)

            session["id"] = user_pass[0]
            session["name"] = user_pass[1]
            session["email"] = user_pass[2]

            flash('You have logged in!', 'success')
            return redirect(url_for('home'))
        flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    session.pop('name', None)
    session.pop('email', None)
    session.pop('id', None)
    return redirect(url_for("home"))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext[0] + f_ext[1]
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
def account():
    if session.get("name"):
        print("Session Started")
        form = UpdateAccountForm()
        if form.validate_on_submit():
            print(form.picture.data)
            if form.picture.data:
                picture_file = save_picture(form.picture.data)
                print(form.picture.data)
                cursor.execute(""" update user_profile set user_pic=%s where user_id=%s""",
                               [picture_file, session["id"]])
            if form.username.data != session["name"]:
                cursor.execute(""" update user_profile set user_name=%s where user_id=%s""",
                               [form.username.data, session["id"]])
                session["name"] = form.username.data
            if form.email.data != session["email"]:
                cursor.execute(""" update user_profile set user_email=%s where user_id=%s""",
                               [form.email.data, session["id"]])
                session["email"] = form.email.data
            conn.commit()
            print("Data Inserted")
            flash('Your account has been updated!', 'info')
            return redirect(url_for('account'))
        elif request.method == 'GET':
            form.username.data = session["name"]
            form.email.data = session["email"]
        cursor.execute(""" select user_pic from user_profile where user_id=%s""", [session["id"]])
        user_image = cursor.fetchone()
        image_file = url_for('static', filename='profile_pics/' + user_image[0])
        return render_template('account.html', title='Account',
                               image_file=image_file, form=form)
    else:
        return redirect(url_for('home'))


def send_reset_email(user_id, user_email):
    token = User_Token.get_reset_token(user_id)
    msg = Message('Password Reset Request',
                  sender='no.reply.yakshblog@gmail.com',
                  recipients=[user_email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    form = RequestResetForm()
    if form.validate_on_submit():
        cursor.execute(''' SELECT user_id from User_Profile 
                                        where user_email=%s''',
                       [form.email.data])
        user_detail = cursor.fetchone()
        print(user_detail)
        send_reset_email(user_detail[0], form.email.data)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    user = User_Token.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        cursor.execute(""" update user_profile set user_pass=%s where user_id=%s""",
                       (hashed_password, user[0]))
        conn.commit()
        flash('Your password has been updated! You are now able to log in', 'info')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)

@app.route("/recommend",methods=['GET','POST'])
def recommend():
    # if session.get("name"):
    #     form = PostForm()
    #     if form.validate_on_submit():
    #         flash('Your Post has been Created','success')
    #         return(redirect(url_for('home')))
        return render_template('Recommend.html',posts=posts)
    # else:
    #     return redirect(url_for('home'))
    
