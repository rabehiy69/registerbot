import os
import csv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# 🔐 Ton token de bot (fourni par BotFather)
BOT_TOKEN = "8543677285:AAGcy1rxfWTD6o5Vv_GTBTc1Fqw7--1bZPo"

# 🖼 Image d'accueil Rainbet (bannière officielle)
RAINBET_IMAGE_URL = "https://rainbet.com/_next/image?url=https%3A%2F%2Fassets.rbgcdn.com%2F223k2P3%2Fraw%2Fbanners%2Fregister-banner.webp&w=3840&q=75"

# 🔗 Ton lien d'affiliation Rainbet (officiel)
RAINBET_SIGNUP_URL = "https://playrainbet.com/tqrk7lopz"

# 🔗 Liens VPN
VPN_IOS_URL = "https://apps.apple.com/fr/app/free-vpn-by-free-vpn-org/id1050171910"
VPN_ANDROID_URL = "https://play.google.com/store/apps/details?id=org.freevpn&hl=fr"

# 👤 Pseudo Telegram de l’admin (sans le @)
ADMIN_USERNAME = "RainbetSupport"

# 📄 Fichier CSV pour tracker les affiliés (ouvrable dans Excel)
AFFILIATES_FILE = "rainbet_affiliates.csv"


def save_affiliate(telegram_id, telegram_username, email, pseudo):
    """
    Sauvegarde les infos dans un CSV (ouvrable dans Excel).
    Colonnes : telegram_id, telegram_username, email, pseudo
    """
    file_exists = os.path.isfile(AFFILIATES_FILE)

    with open(AFFILIATES_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["telegram_id", "telegram_username", "email", "pseudo"])
        writer.writerow([telegram_id, telegram_username, email, pseudo])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    # Menu principal
    keyboard = [
        [InlineKeyboardButton("💰 Accéder au bonus", callback_data="bonus")],
        [InlineKeyboardButton("🆘 J'ai besoin d'aide", callback_data="aide")],
        [InlineKeyboardButton("💎 Découvrir les avantages Rainbet", callback_data="avantages")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_photo(
        chat_id=chat_id,
        photo=RAINBET_IMAGE_URL,
        caption=(
            "🎰 Bienvenue, je vais te guider étape par étape pour t’inscrire sur *Rainbet* 👋\n\n"
            "💸 À la fin du process, tu pourras profiter d’un *bonus de 100%* sur ton dépôt.\n\n"
            "Choisis une option ci-dessous pour commencer 👇"
        ),
        reply_markup=reply_markup,
        parse_mode="Markdown",
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    # ========= BOUTON 1 : ACCÉDER AU BONUS =========

    if data == "bonus":
        keyboard = [
            [InlineKeyboardButton("✅ Oui, j'ai déjà un compte", callback_data="compte_oui")],
            [InlineKeyboardButton("🆕 Non, pas encore", callback_data="compte_non")],
        ]
        await query.message.reply_text(
            "Avant qu’on t’envoie le bonus 💸\n\n"
            "*Tu as déjà un compte Rainbet ?*",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown",
        )

    elif data == "compte_oui":
        keyboard = [
            [InlineKeyboardButton("📲 Tuto VPN", callback_data="vpn_tuto")],
            [InlineKeyboardButton("✅ Continuer la procédure", callback_data="continue_procedure")],
        ]
        text = (
            "🔥 Pour profiter du *bonus 100%*, tu dois créer **un nouveau compte Rainbet** "
            "avec *ce lien* (sinon le bonus ne suit pas) :\n\n"
            f"👉 [Inscris-toi ici]({RAINBET_SIGNUP_URL})\n\n"
            "Si t'es en France ou dans un pays bloqué, il te faut un VPN.\n\n"
            "Tu peux regarder le *Tuto VPN* ou cliquer sur *Continuer la procédure* quand ton compte est prêt 👇"
        )
        await query.message.reply_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown",
        )

    elif data == "compte_non":
        keyboard = [
            [InlineKeyboardButton("📲 Tuto VPN", callback_data="vpn_tuto")],
            [InlineKeyboardButton("✅ Continuer la procédure", callback_data="continue_procedure")],
        ]
        text = (
            "Parfait, t’es au bon endroit 👌\n\n"
            "Pour avoir le *bonus 100%*, inscris-toi avec *ce lien officiel* :\n\n"
            f"👉 [Inscris-toi ici]({RAINBET_SIGNUP_URL})\n\n"
            "Si Rainbet est bloqué chez toi, il te faudra un VPN.\n\n"
            "Tu peux regarder le *Tuto VPN* ou cliquer sur *Continuer la procédure* "
            "une fois que ton compte est créé 👇"
        )
        await query.message.reply_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown",
        )

    elif data == "vpn_tuto":
        text = (
            "🛡 *Tuto VPN pour accéder à Rainbet*\n\n"
            "*Étape 1 – Installer le VPN :*\n"
            "• Télécharge l'application *Free VPN* :\n"
            f"  • iOS : [App Store]({VPN_IOS_URL})\n"
            f"  • Android : [Google Play Store]({VPN_ANDROID_URL})\n\n"
            "*Étape 2 – Se connecter au bon pays :*\n"
            "• Ouvre l'application Free VPN\n"
            "• Choisis un serveur en *Norvège* 🇳🇴\n"
            "  (dans l'app, ça peut être écrit *Scandinavia*)\n"
            "• Clique sur *Connect* pour activer le VPN\n\n"
            "*Étape 3 – Créer ton compte Rainbet :*\n"
            f"• Reviens ici et clique sur : [Inscris-toi ici]({RAINBET_SIGNUP_URL})\n"
            "• Crée ton compte normalement (email, mot de passe, etc.)\n\n"
            "Quand ton compte est créé et ton mail vérifié, tu pourras passer à la suite 💸"
        )
        keyboard_tuto = [
            [InlineKeyboardButton("🏠 Retour au menu principal", callback_data="help_mainmenu")]
        ]
        await query.message.reply_text(text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard_tuto))

        keyboard_q = [
            [InlineKeyboardButton("✅ Oui, j'ai créé mon compte", callback_data="created_yes")],
            [InlineKeyboardButton("❌ Non, pas encore", callback_data="created_no")],
        ]
        await query.message.reply_text(
            "🚀 *As-tu déjà créé ton compte Rainbet ?*",
            reply_markup=InlineKeyboardMarkup(keyboard_q),
            parse_mode="Markdown",
        )

    elif data == "continue_procedure":
        keyboard = [
            [InlineKeyboardButton("✅ Oui, j'ai créé mon compte", callback_data="created_yes")],
            [InlineKeyboardButton("❌ Non, pas encore", callback_data="created_no")],
        ]
        await query.message.reply_text(
            "🚀 *As-tu déjà créé ton compte Rainbet ?*",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown",
        )

    elif data == "created_yes":
        context.user_data["state"] = "WAITING_EMAIL"
        await query.message.reply_text(
            "Nickel ✅\n\n"
            "Envoie-moi maintenant *l'adresse e-mail* que tu as utilisée pour créer ton compte Rainbet :",
            parse_mode="Markdown",
        )

    elif data == "created_no":
        keyboard = [
            [InlineKeyboardButton("✅ Oui, j'ai déjà un compte", callback_data="compte_oui")],
            [InlineKeyboardButton("🆕 Non, pas encore", callback_data="compte_non")],
        ]
        await query.message.reply_text(
            "Pas grave frérot 😉\n\n"
            "*Tu as déjà un compte Rainbet ?*",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown",
        )

    # ========= BOUTON 2 : J'AI BESOIN D'AIDE =========

    elif data == "aide":
        keyboard = [
            [InlineKeyboardButton("📡 VPN / Inscription", callback_data="help_vpn_inscr")],
            [InlineKeyboardButton("💳 Comment déposer", callback_data="help_deposit")],
            [InlineKeyboardButton("💸 Comment retirer ses gains", callback_data="help_withdraw")],
            [InlineKeyboardButton("🏦 Binance & retrait bancaire", callback_data="help_binance")],
            [InlineKeyboardButton("📩 Contacter l'admin", callback_data="help_contact_admin")],
            [InlineKeyboardButton("🏠 Retour au menu principal", callback_data="help_mainmenu")],
        ]
        await query.message.reply_text(
            "🤝 *Centre d'aide Rainbet*\n\n"
            "Choisis ce que tu veux comprendre, je t’explique tranquille 👇",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown",
        )

    elif data == "help_vpn_inscr":
        text = (
            "📡 *VPN + Inscription Rainbet*\n\n"
            "🔹 *1️⃣ Débloquer Rainbet avec un VPN*\n"
            "• Télécharge l'app *Free VPN* :\n"
            f"  • iOS : [App Store]({VPN_IOS_URL})\n"
            f"  • Android : [Google Play Store]({VPN_ANDROID_URL})\n"
            "• Ouvre l'app\n"
            "• Choisis un serveur en *Norvège* 🇳🇴 (*Scandinavia* dans l’app)\n"
            "• Clique sur *Connect*\n\n"
            "🔹 *2️⃣ S'inscrire sur Rainbet*\n"
            f"• Va sur Rainbet via ce lien : [Inscris-toi ici]({RAINBET_SIGNUP_URL})\n"
            "• Clique sur *Register / Inscription*\n"
            "• Remplis le formulaire (email, mot de passe, etc.)\n"
            "• Va dans ta boîte mail et clique sur le lien pour *valider ton adresse e-mail*\n"
            "• Reconnecte-toi ensuite sur Rainbet\n\n"
            "🔹 *3️⃣ Activer une promotion*\n"
            "• Une fois connecté, va dans l'onglet *Promotions*\n"
            "• Choisis une promo qui te correspond\n"
            "• Clique sur *Join / Rejoindre* la promo\n"
            "• Fais ensuite ton dépôt\n\n"
            "Après ça, tu peux commencer à jouer. Bonne chance 🍀"
        )
        keyboard = [
            [InlineKeyboardButton("🏠 Retour au menu principal", callback_data="help_mainmenu")]
        ]
        await query.message.reply_text(text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == "help_deposit":
        text = (
            "💳 *Comment déposer sur Rainbet*\n\n"
            "Tu as deux grandes options : *carte bancaire* ou *cryptomonnaie*.\n\n"
            "🔹 *Option 1 – Dépôt par carte bancaire*\n"
            "• Connecte-toi à ton compte Rainbet\n"
            "• Va dans *Deposit / Dépôt*\n"
            "• Choisis *Card* / *Carte bancaire* (Visa, Mastercard…)\n"
            "• Entre le montant que tu veux déposer\n"
            "• Renseigne les infos de ta carte puis confirme\n"
            "• Le dépôt peut prendre environ *5 à 10 minutes* avant d’apparaître sur ton solde\n\n"
            "🔹 *Option 2 – Dépôt en cryptomonnaie*\n"
            "• Va dans *Deposit / Dépôt*\n"
            "• Choisis *Crypto* ou *Cryptocurrency*\n"
            "• Sélectionne la crypto (USDT, BTC, etc.)\n"
            "• Rainbet te donne une *adresse de dépôt* (et un réseau, ex : TRC20)\n"
            "• Depuis ton wallet (Binance, etc.), envoie tes crypto vers cette adresse\n"
            "• Attends quelques minutes que la transaction soit confirmée\n\n"
            "Une fois le dépôt crédité, tu peux aller dans *Promotions* pour profiter des bonus 🎁"
        )
        keyboard = [
            [InlineKeyboardButton("🏠 Retour au menu principal", callback_data="help_mainmenu")]
        ]
        await query.message.reply_text(text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == "help_withdraw":
        text = (
            "💸 *Comment retirer tes gains depuis Rainbet (version débutant)*\n\n"
            "On va faire simple, étape par étape.\n\n"
            "--------------------------------\n"
            "🧩 1️⃣ Comprendre ce que tu vas faire\n\n"
            "• Rainbet = le site où tu joues\n"
            "• Binance (ou autre) = ton *wallet* / compte crypto\n"
            "• L’idée : tu envoies ton argent de Rainbet ➜ vers ton wallet crypto\n\n"
            "Tu pourras ensuite, depuis ton wallet (ex : Binance), envoyer l’argent vers ton compte bancaire.\n\n"
            "--------------------------------\n"
            "✅ 2️⃣ Avant de faire un retrait\n\n"
            "Avant de demander ton argent :\n"
            "• Vérifie si tu as un *bonus* actif\n"
            "• Si oui, regarde les *conditions du bonus* (wager) dans la page promotion\n"
            "• Si les conditions ne sont pas respectées, ton retrait peut être bloqué ou refusé\n\n"
            "Une fois que tout est bon : tu peux passer au retrait.\n\n"
            "--------------------------------\n"
            "🏦 3️⃣ Aller sur la page de retrait Rainbet\n\n"
            "• Connecte-toi à ton compte Rainbet\n"
            "• Va dans le menu *Withdraw / Retrait*\n"
            "• Choisis la méthode de retrait : en général, *Crypto* (cryptomonnaie)\n\n"
            "--------------------------------\n"
            "🪙 4️⃣ Choisir la crypto pour ton retrait\n\n"
            "• Sur Rainbet, tu vas devoir choisir une crypto :\n"
            "  – Par exemple : *USDT*, *BTC*, etc.\n"
            "• Le plus simple pour les débutants : souvent *USDT* sur le réseau *TRC20*\n\n"
            "👉 Garde bien en tête :\n"
            "• Crypto choisie sur Rainbet = crypto que tu devras choisir aussi sur ton wallet\n"
            "• Réseau choisi sur Rainbet = même réseau sur ton wallet (TRC20, ERC20…)\n\n"
            "--------------------------------\n"
            "📲 5️⃣ Récupérer ton adresse de réception (sur Binance par exemple)\n\n"
            "• Ouvre ton application *Binance*\n"
            "• Va dans *Dépôt / Deposit*\n"
            "• Choisis la même crypto que sur Rainbet (ex : USDT)\n"
            "• Choisis le même réseau (ex : TRC20)\n"
            "• Binance t’affiche une *adresse* (une longue suite de lettres/chiffres)\n"
            "• Copie cette adresse (bouton *Copy / Copier*)\n\n"
            "--------------------------------\n"
            "📥 6️⃣ Coller l’adresse sur Rainbet et lancer le retrait\n\n"
            "• Retourne sur Rainbet, dans la page *Withdraw / Retrait*\n"
            "• Colle l’adresse que tu as copiée depuis Binance\n"
            "• Vérifie bien :\n"
            "  – La crypto est la même des deux côtés (USDT partout, par ex)\n"
            "  – Le réseau est le même (TRC20 des deux côtés, par ex)\n"
            "• Entre le montant que tu veux retirer\n"
            "• Valide le retrait\n\n"
            "--------------------------------\n"
            "⏳ 7️⃣ Temps de traitement (très rapide)\n\n"
            "• Sur Rainbet, les retraits crypto sont *très rapides*\n"
            "• En pratique :\n"
            "  – Selon la crypto et le réseau, ça prend souvent entre *quelques secondes* et *5 à 10 minutes max*\n"
            "  – Si tu vois un petit délai, c’est normal, le temps que la blockchain confirme la transaction\n\n"
            "Dès que c’est validé, tu verras la transaction apparaître dans l’historique de ton wallet (ex : Binance).\n\n"
            "--------------------------------\n"
            "🏁 8️⃣ Et après ?\n\n"
            "Une fois l’argent arrivé sur ton wallet (Binance) :\n"
            "• Tu peux convertir ta crypto en euros (EUR)\n"
            "• Puis faire un virement vers ton compte bancaire\n\n"
            "Pour ça, regarde le tuto *Binance & retrait bancaire* dans le centre d’aide 🏦."
        )
        keyboard = [
            [InlineKeyboardButton("🏠 Retour au menu principal", callback_data="help_mainmenu")]
        ]
        await query.message.reply_text(text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == "help_binance":
        text = (
            "🏦 *De Rainbet à ton compte bancaire via Binance*\n\n"
            "🔹 *1️⃣ Créer un compte Binance*\n"
            "• Télécharge l'app Binance\n"
            "• Crée un compte avec ton email\n"
            "• Vérifie ton identité (KYC) si demandé\n\n"
            "🔹 *2️⃣ Recevoir les crypto depuis Rainbet*\n"
            "• Sur Binance, va dans *Dépôt Crypto*\n"
            "• Choisis la même crypto que sur Rainbet (ex : USDT)\n"
            "• Choisis le *même réseau* (TRC20, ERC20, etc.)\n"
            "• Copie ton adresse de dépôt Binance\n"
            "• Colle cette adresse dans le retrait cryptomonnaie sur Rainbet\n"
            "• Valide le retrait et attends la réception sur Binance\n\n"
            "🔹 *3️⃣ Convertir en euros (EUR)*\n"
            "• Une fois les crypto arrivées sur Binance, va dans *Convertir* ou *Trader*\n"
            "• Échange USDT/BTC contre de l’*EUR*\n\n"
            "🔹 *4️⃣ Retirer vers ton compte bancaire*\n"
            "• Va dans *Portefeuille > Retrait > Fiat (EUR)*\n"
            "• Choisis *Virement bancaire (SEPA)*\n"
            "• Ajoute ton RIB si besoin\n"
            "• Entre le montant à retirer puis confirme\n\n"
            "Les virements SEPA sont souvent rapides, parfois quasi instantanés selon la banque 💶."
        )
        keyboard = [
            [InlineKeyboardButton("🏠 Retour au menu principal", callback_data="help_mainmenu")]
        ]
        await query.message.reply_text(text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == "help_contact_admin":
        text = (
            "📩 *Besoin d’un humain ?*\n\n"
            f"Tu peux écrire directement à l’admin ici : *@{ADMIN_USERNAME}*\n\n"
            "Explique ton problème (inscription, dépôt, retrait, bonus…) et envoie un screen si besoin."
        )
        keyboard = [
            [InlineKeyboardButton("🏠 Retour au menu principal", callback_data="help_mainmenu")]
        ]
        await query.message.reply_text(text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == "help_mainmenu":
        # Retour au menu principal
        await start(update, context)

    # ========= BOUTON 3 : AVANTAGES =========

    elif data == "avantages":
        text = (
            "💎 *Pourquoi Rainbet, c’est intéressant ?*\n\n"
            "🌍 *Réputation & popularité*\n"
            "• L’un des casinos crypto les plus reconnus au monde\n"
            "• Très utilisé par des parieurs US et internationaux\n"
            "• Casino très populaire aux États-Unis 🇺🇸\n\n"
            "💸 *Retraits en crypto*\n"
            "• Retraits en cryptomonnaie très rapides\n"
            "• Souvent quasi instantanés ou quelques minutes selon la crypto\n"
            "• Pas de petits plafonds de retrait qui te bloquent\n\n"
            "🥊 *Partenaire de Ryan Garcia*\n"
            "• Ryan Garcia = boxeur professionnel américain\n"
            "• Ancien champion intérim WBC des poids légers\n"
            "• Connu pour sa vitesse, son style spectaculaire et ses gros combats médiatisés\n"
            "• Star des réseaux avec des millions d’abonnés\n\n"
            "📈 *Paris sportifs*\n"
            "• Cotes très compétitives sur les gros matchs\n"
            "• Beaucoup plus de types de paris dispo : handicaps, buteurs, combinés, paris live, eSports, etc.\n\n"
            "🎰 *Casino & RTP élevé*\n"
            "• Enorme catalogue de jeux : slots, live casino, jeux originaux (Plinko, Mines, Crash, etc.)\n"
            "• Beaucoup de jeux affichent un *RTP* (Return To Player) très élevé\n\n"
            "🧠 *C’est quoi le RTP ?*\n"
            "• Le RTP (*Return To Player*) = pourcentage théorique que le jeu rend aux joueurs sur le long terme\n"
            "• Exemple : RTP 97% ➜ sur 100€ misés, le jeu rend en moyenne 97€ aux joueurs (sur des milliers de mises)\n"
            "• Plus le RTP est élevé, plus le jeu est “avantageux” pour le joueur sur la durée\n\n"
            "Rainbet met en avant plusieurs jeux avec des RTP très hauts (certains montent jusqu’à ~99%), "
            "ce qui est largement mieux que les petits casinos éclatés 👀\n\n"
            "En résumé : plus de choix, de meilleures cotes, des retraits rapides.\n"
            "À toi de voir comment tu en profites 😉"
        )
        keyboard = [
            [InlineKeyboardButton("🏠 Retour au menu principal", callback_data="help_mainmenu")]
        ]
        await query.message.reply_text(text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))


async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Gère les messages texte quand on attend l'email ou le pseudo.
    """
    state = context.user_data.get("state")

    # On attend l'email
    if state == "WAITING_EMAIL":
        email = update.message.text.strip()
        context.user_data["email"] = email
        context.user_data["state"] = "WAITING_PSEUDO"

        await update.message.reply_text(
            "Parfait 🙏\n\n"
            "Maintenant envoie-moi *ton pseudo Rainbet* (le nom que tu vois sur le site) :",
            parse_mode="Markdown",
        )

    # On attend le pseudo
    elif state == "WAITING_PSEUDO":
        pseudo = update.message.text.strip()
        email = context.user_data.get("email")
        user = update.effective_user

        telegram_id = user.id
        telegram_username = user.username or ""

        # Sauvegarde dans le CSV
        save_affiliate(telegram_id, telegram_username, email, pseudo)

        # Reset state
        context.user_data["state"] = None
        context.user_data["email"] = None

        # Explication des bonus une fois les infos enregistrées
        text = (
            "Top, j’ai bien enregistré tes infos ✅\n\n"
            "Ton compte est maintenant bien relié pour le *bonus Rainbet*.\n"
            "Il te suffit de choisir et d’activer la promo qui te correspond dans l’onglet *Promotions*.\n\n"
            "🎁 *Comment activer ton bonus sur Rainbet ?*\n\n"
            "🔹 *Option 1 – Bonus en 3 dépôts (40x mise verrouillée)*\n\n"
            "• 1er dépôt : Bonus de 100% + 20 tours gratuits\n"
            "• 2ème dépôt : Bonus de 50% + 20 tours gratuits\n"
            "• 3ème dépôt : Bonus de 100% + 20 tours gratuits\n\n"
            "👉 Comment ça marche :\n"
            "• Tu t'inscris à la promotion qui te correspond\n"
            "• Tu fais ton dépôt\n"
            "• Tu utilises *tous* tes tours gratuits\n"
            "• Tu joues le bonus jusqu'à remplir les conditions (le wager)\n"
            "• Quand un niveau est terminé, le suivant se débloque avec ton prochain dépôt\n\n"
            "🔹 *Option 2 – Bonus sans pari verrouillé*\n\n"
            "• Ton argent reste plus libre\n"
            "• Tu peux avoir jusqu’à *100% de bonus*\n"
            "• Le bonus se débloque petit à petit à chaque pari que tu fais\n\n"
            "💡 *En résumé :*\n"
            "• Tu veux un gros boost direct + des free spins ➜ prends la *première offre*\n"
            "• Tu veux plus de flexibilité et garder ton argent plus libre ➜ prends la *deuxième offre*\n\n"
            "Et surtout : *inscris-toi à la promo avant de déposer*, sinon le bonus ne s’active pas 😉"
        )

        await update.message.reply_text(text, parse_mode="Markdown")

        # Deuxième message de vibe / encouragement + bouton retour menu
        keyboard = [
            [InlineKeyboardButton("🏠 Retour au menu principal", callback_data="help_mainmenu")]
        ]
        await update.message.reply_text(
            "Tout est bon de mon côté ✅\n\n"
            "Bonne chance sur Rainbet, j’espère que tu claques un gros jackpot bientôt 💰🍀",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    else:
        # Pas d'état particulier → on peut ignorer
        pass


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))

    print("Bot lancé 🚀")
    app.run_polling()


if __name__ == "__main__":
    main()
