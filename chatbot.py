from flask import Blueprint, request, jsonify, render_template
import spacy

chatbot_bp = Blueprint("chatbot", __name__)

# Carrega modelo de linguagem
nlp = spacy.load("en_core_web_sm")

# Base de conhecimento simples (FAQ)
faq = { 
    # Saudações
    "oi": "Oiie! Seja bem-vindo(a) à Confeitaria Gatito! Me chamo Nino e estou aqui para auxiliar. 😺🍰",
    "olá": "Oláaa! Que bom te ver por aqui! Me chamo Nino e estou aqui para auxiliar. 😺🍰 ✨",
    "hey": "Hey! How can I help you today? 😺",
    "hi": "Hi! Welcome to Gatito Confectionery! My name is Nino and I'm here to help. 😺🍰",
    "e aí": "E aíí! Tudo suave? 😎",
    "nino": "Eu aqui!! Como posso ajudar? 😎",
    "nino faz bolo": "Eu adoraria! Mas deixo isso para as confeiteiras profissionais. Eu fico nos bastidores dando aquela ajudinha mágica! 😺✨",
    "doce favorito do nino": "Aaaah, difícil escolher! Mas cupcakes de morango são meu ponto fraco. 😺🧁🍓",
    "nino trabalha aqui": "Trabalho sim! Sou o mascote e quase dono da Confeitaria Gatito. 😺🧁",
    "nino é fofo": "Aaaah, eu? Fofinho? Talvez só um pouquinho… 😸💗",
    "nino pode ajudar": "Com certeza! O que você precisa? 😺✨",
    "qual o trabalho do nino": "Sou o assistente virtual da Confeitaria Gatito! Te ajudo com pedidos, dúvidas, cardápio e recomendações. 😺🍰",
    "quantos anos nino tem": "Idade? Hmmm… gatos não contam assim! Eu tenho exatamente a quantidade de anos necessária para ser fofinho! 😺💖",
    "o que nino faz": "Eu ajudo você com dúvidas, recomendação de produtos e qualquer coisinha da Confeitaria Gatito! 😺✨",
    "quem é nino": "Eu sou o Nino! 🐱🎂 O gatinho assistente da Confeitaria Gatito. Estou aqui para ajudar você a escolher os doces mais deliciosos!",
    "hello": "Hi! Welcome to Gatito Confectionery! My name is Nino and I'm here to help. 😺🍰",
    "opa": "Opa, tudo bem? Como posso ajudar? Me chamo Nino e estou aqui para auxiliar. 😺🍰",
    "boa tarde": "Boa tarde! 🌞 Como posso adoçar seu dia?  Me chamo Nino e estou aqui para auxiliar. 😺🍰",
    "boa noite": "Boa noite! ✨ Que doce você procura? Me chamo Nino e estou aqui para auxiliar. 😺🍰",
    "bom dia": "Bom diaaa! 🌻 Já escolheu seu bolo hoje?",

    # Produtos
    "quais produtos vocês vendem": "Temos bolos, cupcakes, docinhos e sobremesas artesanais deliciosas! 😋",
    "o que vocês vendem": "Vendemos diversos doces artesanais, dá uma olhadinha no cardápio!",
    "produtos": "Temos bolos, doces, sobremesas e muito mais. Tudo feito com amor! 💛",
    "tem bolo": "Claro que tem! Temos muitos tipos de bolo fresquinhos!",
    "quais bolos": "Temos bolos caseiros, naked cake, bolo gelado, bolo vulcão… só escolher!",
    "cupcake": "Temos cupcakes lindos e deliciosos! 🧁",
    "doces": "Tem docinho sim! Brigadeiro, beijinho, cajuzinho e muito mais! 🍬",
    "menu": "Nosso menu inclui bolos, cupcakes e doces artesanais.",
    "cardápio": "O cardápio está recheado de delícias! 😍",

    # Pagamento
    "formas de pagamento": "Aceitamos Pix, cartão e dinheiro! 💸",
    "pode pagar no pix": "Pode sim! Pix liberado 😄",
    "aceita cartão": "Aceitamos cartão sim, débito e crédito!",
    "pagamento": "Temos Pix, cartão e dinheiro.",
    "pix": "Pix aceitamos sim! 🔥",
    "visa": "Aceitamos Visa, MasterCard e mais!",
    "cartões": "Aceitamos Visa, MasterCard e mais!",
    "cartao": "Aceitamos Visa, MasterCard e mais!",


    # Entrega
    "como funciona a entrega": "A entrega é super simples! Você faz o pedido, nós preparamos tudo com carinho e levamos até você. 😺🚚✨",
    "qual o valor da entrega": "A taxa de entrega depende da região! Posso verificar pra você. 😺📍",
    "taxa de entrega": "A taxa varia conforme o bairro. Quer me informar sua região?",
    "entrega hoje": "Entregamos sim! Dependendo do horário e da disponibilidade. Quer confirmar comigo? 😺🕒",
    "tem entrega hoje": "Temos sim! Só me diga o bairro. 😺📦",
    "entrega no mesmo dia": "Entregamos no mesmo dia para pedidos feitos com antecedência! 🕒✨",
    "faz entrega agora": "Posso verificar a disponibilidade para você! 😺",
    "entrega rápida": "Temos entrega rápida dependendo da região! 🚀",
    "faz entrega domingo": "Entregamos aos domingos em horários especiais! 😺📆",
    "faz entrega sábado": "Sim! Sábados são dias de muito movimento, mas entregamos sim! 😺✨",
    "entrega funciona que horas": "Nossa entrega funciona das 9h às 18h! ⏰💛",
    "entrega até que horas": "Entregamos até as 18h! 😺📦",
    "qual o horário da entrega": "Nossas entregas são realizadas das 9h às 18h! ⏰💕",
    "posso agendar entrega": "Pode sim! Agendamos horários conforme disponibilidade. 😺📅",
    "entrega agendada": "Realizamos entregas agendadas direitinho! 😺📆✨",
    "entrega demorou": "Poxa! Me desculpa por isso 😿. Quer me passar o número do pedido pra eu verificar?",
    "entrega atrasou": "Ops! Vou verificar pra você agora mesmo. 😿💞",
    "demora para entregar": "Normalmente não! Entregamos bem rapidinho dependendo da região. 😺🚚✨",
    "entrega em quanto tempo": "Depende do bairro, mas geralmente é bem rapidinho! 😺💨",
    "entrega para qual região": "Entregamos em Campinas e região! 📍💕",
    "entrega para outros bairros": "Provavelmente sim! Quer me informar o nome do bairro? 😺",
    "faz entrega na minha região": "Me fala seu bairro e eu confirmo rapidinho! 😺✨",
    "entrega aqui": "Me passa o nome do bairro e eu te digo já! 😺📍",
    "faz delivery na minha casa": "Provavelmente sim! Só me diga a região. 😺🏡",
    "entrega por motoboy": "Sim! Trabalhamos com motoboys parceiros super confiáveis. 😺🏍️",
    "entrega grátis disponíveis": "Temos entrega grátis para compras acima de R$ 100. 😺🎉",
    "como conseguir entrega grátis": "É só fazer compras acima de R$ 100 que a entrega sai por nossa conta! 😺❤️",
    "faz entrega com taxa": "Sim! A taxa depende da sua região. Me passa o bairro?",
    "calcular entrega": "Claro! Me diga seu bairro que eu calculo. 😺📍",
    "valor da entrega para meu bairro": "Só me diga qual é o bairro e eu te digo! 😺✨",
    "entrega via ifood": "Ainda não! Nosso delivery é próprio, bem mais cuidadoso. 😺💖",
    "entrega é segura": "Com certeza! Nosso motoboy leva tudo embalado com carinho. 😺📦💗",
    "pode deixar na portaria": "Claro! Só avisar na hora do pedido. 😺🔑",
    "entrega sem contato": "Fazemos sim, é só pedir! 😺✨",
    "posso acompanhar a entrega": "Pode sim! Te enviamos atualizações pelo WhatsApp. 😺📲",
    "quem faz a entrega": "Motoboys parceiros super cuidadosos! 😺🏍️💛",


    # Frete
    "frete": "O frete depende da região, mas acima de R$ 200 é grátis! 😺🚚✨",
    "valor do frete": "O valor varia conforme o bairro. Me fala sua região e eu te digo! 😺📍",
    "frete grátis": "Simm! Frete grátis para compras acima de R$ 200. 🎉💛",
    "tem frete grátis": "Temos! Acima de R$ 200 o frete é por nossa conta. 😺✨",
    "quanto custa o frete": "Depende do bairro! Me conta qual é o seu que eu confirmo. 📍😺",
    "qual o frete para meu bairro": "Me passa o nome do bairro e eu calculo rapidinho! 😺💨",
    "qual a taxa de entrega": "A taxa varia pela distância, mas posso verificar pra você! 📍✨",
    "taxa de entrega cara": "Ela muda conforme o bairro, mas sempre tentamos deixar o mais justo possível. 😺💛",
    "tem taxa de entrega": "Tem sim, mas acima de R$ 200 é grátis! 😺🎉",
    "cobram frete": "Cobramos sim, mas depende da região. Acima de R$ 200 não paga nada! 😺✨",
    "frete caro": "Poxa 😿 depende da distância… mas prometo que vale pelo sabor! 💛",
    "frete barato": "Tentamos manter sempre o mais acessível possível! 😺💖",
    "quanto tá o frete hoje": "Mesma regra de sempre! Depende da região, me manda o bairro. 😺📦",
    "como funciona o frete": "Super simples! Calculamos pela distância e acima de R$ 200 sai grátis. 😺✨",
    "frete compensa": "Com certeza! Ainda mais se bater R$ 200 que fica de graça hehe 😺💛",
    "frete grátis hoje": "Frete grátis para compras acima de R$ 200, sempre! 🎉😉",
    "tem desconto no frete": "Acima de R$ 200 fica zerado! 😺✨",
    "frete atende minha região": "Provavelmente sim! Me passa o nome do bairro que eu confirmo. 📍😺",
    "quanto fica o frete para aqui": "Me diga seu bairro que eu calculo na hora! 😺💫",
    "frete região tal": "Me manda o nome certinho do bairro e te informo rapidinho. 😺💨",
    "frete calculado por km": "Ele é calculado pela distância, sim! 📍🚚",
    "frete calculado pela distância": "Isso! Quanto mais longe, maior a taxa… mas acima de R$ 200 é free! 😺🎉",
    "entrega com frete grátis": "Sim! Compras acima de R$ 200 não pagam frete. 😉✨",
    "tem taxa mínima": "A taxa depende só da distância mesmo! 😺📍",
    "posso saber o frete": "Claro! Só me passar o bairro que eu confirmo. 😺💗",
    "frete Campinas": "Em Campinas varia por bairro! Me diz o seu. 😺📍",
    "frete região metropolitana": "Atendemos várias regiões próximas! Me envia o nome do bairro. 😺✨",
    "frete é fixo": "Não, ele muda conforme o bairro! Mas acima de R$ 200 é sempre grátis. 😺💕",
    "é grátis acima de quanto": "Acima de R$ 200 o frete sai na faixa! 😺🎉",
    "free shipping": "Yes! Free shipping for orders above R$ 200! 😺🚚✨",
    "delivery fee": "Our delivery fee depends on your location. 😺📍",
    "shipping cost": "It varies by distance! Tell me your neighborhood. 😺💬",

    # Pedidos
    "como faço pedido": "Super fácil! Só escolher o produto, colocar na sacola e finalizar. Se quiser, te guio! 😺🛍️",
    "pedido": "Quer fazer um pedido? Me fala o que você quer e eu te ajudo rapidinho! 😺✨",
    "quero comprar": "Amoo! 😺💖 Me diz o que você quer que te explico como pedir.",
    "posso pedir bolo": "Claro que pode! É só escolher o bolo e finalizar o pedido na sacolinha 😋🎂",
    "como faço um pedido": "Você escolhe o produto → adiciona à sacola → finaliza. Facinho! 💛",
    "como comprar": "Só adicionar o produto na sacola e finalizar o pedido! Posso te guiar se quiser 😺🛍️",
    "quero fazer um pedido": "Obaaa! 💖 O que você gostaria de pedir hoje?",
    "quero pedir": "Prontíssimo pra te ajudar! O que você deseja? 😺✨",
    "como funciona o pedido": "Você escolhe, coloca na sacola e finaliza. Bem simples! 🛒💕",
    "pode fazer pedido por aqui": "Por aqui eu te ajudo com infos! O pedido oficial é feito no site pelo carrinho 😺✨",
    "aceita pedido pelo chat": "Eu dou suporte, mas o pedido é finalizado pelo site, tá? 😺💬",
    "fazer pedido pelo site": "Isso mesmo! Escolhe o item e finaliza na sacola. Facinho! 😸🛍️",
    "quero pedir um bolo": "Delíciaaaa 😻🎂 Qual tipo você quer?",
    "como peço um doce": "Escolhe o doce → adiciona à sacola → finaliza o pedido. Posso te acompanhar! 🍬😺",
    "pedido mínimo": "Não temos valor mínimo! Pode pedir o que quiser 😺✨",
    "como fechar pedido": "É só ir na sacola e clicar em finalizar ✨",
    "como finalizo compra": "Só acessar a sacola no canto da tela e finalizar. Precisa de ajuda? 😺🛍️",
    "não consigo fazer pedido": "Ihh 😿 me conta o que tá acontecendo que eu te ajudo a resolver!",
    "não aparece sacola": "Talvez seja um bug! Atualiza a página e tenta de novo 😺💛",
    "tá dando erro no pedido": "Poxa 😿 me conta qual erro aparece que te ajudo!",
    "pedido rápido": "Se quiser agilidade, já me diga o que quer que te ajudo a ir direto! ⚡😺",
    "checkout": "O checkout é feito pela sacola! Só clicar e finalizar 😺✨",
    "como é o processo de pedido": "Escolhe → adiciona → finaliza → recebe! Facinho 😺🍰",
    "consigo pedir agora": "Simm! Escolhe seu doce ou bolo e boraaa! 😺💖",
    "quero comprar agora": "Perfeito! Qual o item da sua vez? 😺✨",
    "tá aberto pra pedido": "Tô aqui 24h! O site também aceita pedidos sempre 😺💬",
    "aceita encomenda": "Simm! Para encomendas personalizadas, temos um formulário especial ✨🎂",
    "posso encomendar": "Pode sim! Quer algo personalizado? 😺💗",
    "encomenda": "Fazemos encomendas personalizadas! Quer saber como funciona?",
    "fazer encomenda": "Para encomendas especiais, você pode usar o formulário na aba de contato! 😺✨",
    "quero personalizar": "Amoo! 💖 Me diga como quer seu bolo e te digo o processo certinho.",
    "order": "You can place your order through the cart! Need help? 😺🍰",
    "how to order": "Just choose the product, add to cart and finish the checkout! 😺✨",
    "can i order": "Sure! Just pick what you want and add it to your cart 😸🛍️",
    "make an order": "You can place your order through the website! Want help choosing? 😺💛",
    "how do i buy": "Add the product to the cart and finish the checkout. Easy! 😺✨",
    "purchase": "Purchases are made through the sacola/carrinho! Need help? 😺🛍️",
    "comprar": "Para comprar é só jogar na sacola e finalizar! 😺✨",
    "posso comprar aqui": "Aqui eu te ajudo com infos! A compra de verdade é finalizada pela sacola 😺💖",


    # Personalização
    "bolo personalizado": "Fazemos bolo personalizado sim! 🎂✨ Me diz o tema e já te explico como funciona.",
    "personalizar": "Pode personalizar sim! Me manda o tema, cor, referência ou até foto que eu te ajudo! 😺🎨",
    "fazer bolo sob medida": "Claro que fazemos! Só me dizer o estilo que você quer que te passo os detalhes ✨",
    "quero um bolo personalizado": "Amoo quando pedem isso!! 😻🎂 Me conta o tema!",
    "vocês fazem bolo personalizado": "Simmm! De vários temas, estilos e tamanhos 😺🎉",
    "posso personalizar o bolo": "Pode sim! Só enviar o que tiver em mente 😺💖",
    "como personalizar": "Você me manda o tema ou uma referência e faço tudo direitinho pra você 🎂✨",
    "aceitam encomenda personalizada": "Aceitamos sim! É só mandar o tema e combinar os detalhes 😸",
    "bolo temático": "A gente faz qualquer tema! Princesas, super-heróis, floral, minimalista… só escolher 😺🎂",
    "tema do bolo": "Me diz o tema que você quer e eu te ajudo com ideias 💡🎂",
    "quero mandar referência": "Pode mandar! Quanto mais detalhado, melhor 😺💖",
    "quero enviar foto": "Pode enviar a fotinho da inspiração! Isso ajuda muito 🎂📸",
    "vocês fazem bolo de aniversário personalizado": "Sim! E fica lindooo 😻🎉",
    "faz bolo decorado": "Fazemos sim! Desde simples até super elaborados ✨🎂",
    "façam bolo 3d": "Fazemos bolos 3D também! Só mandar a ideia 😺💛",
    "aceita foto de inspiração": "Siiiim! Pode mandar a vontade 😺📸",
    "pode copiar um bolo": "Podemos fazer algo inspirado! ✨ Sempre mantendo o nosso estilo 😺",
    "posso escolher o sabor": "Pode sim! A personalização inclui sabor, recheio e decoração 😸🎂",
    "quais temas vocês fazem": "Todos! Anime, casamento, infantil, minimalista, elegante, tudo mesmo 😺✨",
    "quero algo exclusivo": "A gente cria do zero pra você! 🧁💛 Só dizer o estilo e tema.",
    "personalização é paga": "Depende do nível de detalhe! Mas te passo o orçamento certinho 😊",
    "quanto custa personalizar": "O valor varia do tamanho e da decoração! Me diz o tema pra te dar uma ideia 😺💰",
    "orçamento bolo personalizado": "Me manda o tema, tamanho e uma referência que faço o orçamento 💛🎂",
    "quero decorado": "Beleza! Qual estilo de decoração você quer? 😺✨",
    "fazer bolo a gosto": "Fazemos sim! Do jeitinho que você imaginar 🎂💭",
    "personalização complexa": "Pode mandar!! A gente ama um desafio 😺🔥🎨",
    "vocês fazem topo de bolo": "Simm! Fazemos topinhos simples ou personalizados 🎀✨",
    "bolo com nome": "Claro! Podemos colocar nome, idade, frase… o que quiser 😺✨",
    "bolo com foto": "Sim! Fazemos bolo com foto comestível também 🎂🖼️",
    "custom cake": "Yes! We do custom cakes! Tell me the theme 😺🎂",
    "can i customize": "Sure! Just send me the theme or a reference 💛",
    "customized cake": "We make fully customized cakes! 🎂✨",
    "i want a custom cake": "Amazing! Tell me the theme or style and I'll help 😺🎨",
    "tema personalizado": "Manda o tema que você quer que eu te ajudo com tudo 💛🎂",
    "quero bolo diferente": "Adorooo! Me conta como você imaginou 😺🔥✨",
    "bolo exclusivo": "Fazemos bolos exclusivos sim! Só mandar sua ideia ✨🎂",

    # Horário
    "horário": "Funcionamos todos os dias, das 8h às 19h! 🕒 Qualquer dúvida é só chamar!",
    "horarios": "Estamos por aqui das 8h às 19h, todos os dias 😺✨",
    "que horas abre": "Abrimos às 8h da manhã! 🌞",
    "que horas fecha": "Fechamos às 19h 🕖💛",
    "hora de funcionamento": "Estamos abertos das 8h às 19h, todos os dias!",
    "horário de funcionamento": "Funcionamos diariamente das 8h às 19h! 😺",
    "abre que horas": "Abrimos às 8h certinho! ⏰",
    "fecha que horas": "Fechamos às 19h! ✨",
    "aberto": "Estamos abertooos! Funcionamento das 8h às 19h 😺💕",
    "ta aberto": "Tamo aberto sim! Das 8h às 19h 😎",
    "tá aberto agora": "Se for entre 8h e 19h, tamo on! 😺✨",
    "vocês estão abertos": "Estamos sim, das 8h às 19h! 🕒",
    "funcionamento": "Funcionamos todos os dias até as 19h ❤️",
    "horário hoje": "Hoje? Mesmo horário: 8h às 19h! 🌞✨",
    "abre domingo": "Sim! Abrimos todos os dias, inclusive domingo 😺🎉",
    "funciona fim de semana": "Funciona sim! Todo dia das 8h às 19h 💕",
    "abre feriado": "Quase todos os feriados ficamos abertos, mas depende! Melhor confirmar no dia 😉",
    "estão abertos agora": "Se for entre 8h e 19h, sim! 😺💛",
    "horário gatito": "A Gatito funciona das 8h às 19h todos os dias! 🍰✨",
    "horário atendimento": "Nosso atendimento funciona de 8h às 19h! 😸💬",
    "o nino trabalha quando": "Eu trabalho 24/7 na magia da internet 😎✨ Mas a confeitaria é das 8h às 19h!",
    "horário loja": "A loja física funciona das 8h às 19h 🕒",
    "quando abre": "A gente abre às 8h! 🌞",
    "quando fecha": "Fechamos às 19h, mas o Nino sempre fica por aqui 😺✨",
    "estão funcionando": "Sim! Funcionamos todos os dias das 8h às 19h 💖",
    "horário de atendimento hoje": "Hoje é das 8h às 19h! Sempre esse horário 😺",


    # Localização
    "onde ficam": "Estamos na Rua das Flores, 123 – Campinas 🌸✨",
    "endereço": "Nosso endereço é Rua das Flores, nº 123, Campinas! 💕",
    "localização": "Estamos localizados em Campinas, na Rua das Flores 🌼",
    "onde é": "Fica na Rua das Flores, pertinho do centro! 😺📍",
    "onde fica a loja": "Nossa loja fica na Rua das Flores, nº 123! 🍰",
    "como chegar": "É só seguir em direção ao centro de Campinas e procurar a Rua das Flores 🌸",
    "onde fica": "Ficamos na Rua das Flores, 123 – bem fácil de achar! 📍",
    "onde estão": "Estamos na Rua das Flores, 123 – Campinas 💕",
    "qual o endereço": "Rua das Flores, 123 🌸 Te espero lá!",
    "location": "We're located at Rua das Flores, 123 – Campinas! 📍✨",
    "whats the address": "Our address is Rua das Flores, 123 — Campinas 💛",
    "mapa": "No mapa, é só buscar ‘Confeitaria Gatito’ na Rua das Flores 🌸📍",
    "onde é a confeitaria": "A confeitaria fica na Rua das Flores, 123, Campinas! 😺✨",
    "ponto de referência": "Ponto de referência? Ficamos perto do centro de Campinas! 🌆",


    # Agradecimentos
    "obrigado": "Imaginaaa! Qualquer coisa chama o Nino 😺💖",
    "obrigada": "Por nadaaa! Tô sempre por aqui 💕",
    "vlw": "Tamo junto demais! 😎✨",
    "valeu": "Valeuu! Qualquer coisa, só me chamar 🐾",
    "thanks": "You're welcome! 😄💛",
    "thank you": "You're super welcome! 😺✨",
    "obg": "De nadaaa! 💗",
    "brigado": "Disponha! 😸",
    "valeu nino": "Valeu vocêee! 😺💕",
    "muito obrigado": "Eu que agradeço! 😺✨",
    "tmj": "TMJ sempre! 😎🔥",
    "agradecido": "De nada! Sempre bom ajudar 😺",
    "thanks nino": "Anytime! Nino is always here 😺💛",
    "thank u": "You're welcomeee! ✨",
    "obrigadão": "Obaaaa! Precisando, só chamar! 💖",
}

def buscar_resposta(pergunta):
    pergunta_proc = nlp(pergunta.lower())

    melhor_resposta = "Desculpe, não entendi. Pode repetir? 😊"
    maior_similaridade = 0.45  # limite menor → chatbot entende mais coisas

    for chave, resposta in faq.items():
        chave_proc = nlp(chave.lower())
        similaridade = chave_proc.similarity(pergunta_proc)

        if similaridade > maior_similaridade:
            maior_similaridade = similaridade
            melhor_resposta = resposta

    return melhor_resposta

@chatbot_bp.route("/chat")
def chat_page():
    return render_template("chat.html")

@chatbot_bp.route("/chatbot", methods=["POST"])
def chat():
    data = request.get_json()
    pergunta = data.get("mensagem", "")
    resposta = buscar_resposta(pergunta)
    return jsonify({"resposta": resposta})


