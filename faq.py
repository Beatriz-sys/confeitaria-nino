from flask import Blueprint, render_template

faq_bp = Blueprint("faq", __name__)

# Lista de perguntas e respostas – expandida
faq_perguntas = [
    # -----------------------------
    # PEDIDOS
    # -----------------------------
    {
        "pergunta": "Como faço um pedido?",
        "resposta": "Você pode escolher o produto desejado na página de produtos, adicionar à sacola e finalizar o pedido no menu 'Sacola'."
    },
    {
        "pergunta": "Quero comprar, como faço?",
        "resposta": "É só escolher o produto, colocar na sacola e finalizar! Qualquer dúvida, é só chamar o suporte."
    },
    {
        "pergunta": "Preciso criar conta para pedir?",
        "resposta": "Não! Você pode comprar sem criar conta. Criar conta apenas facilita para ver histórico de pedidos."
    },

    # -----------------------------
    # PERSONALIZAÇÃO
    # -----------------------------
    {
        "pergunta": "Posso personalizar um bolo?",
        "resposta": "Sim! Entre em contato pelo formulário de contato e descreva o sabor, tema e decoração desejada."
    },
    {
        "pergunta": "Vocês fazem bolo temático?",
        "resposta": "Fazemos sim! Envie sua referência ou explique o tema que criamos do jeitinho que você quiser."
    },
    {
        "pergunta": "Qual antecedência preciso para bolo personalizado?",
        "resposta": "Recomendamos pelo menos 3 dias de antecedência para garantir disponibilidade e capricho na decoração."
    },

    # -----------------------------
    # PAGAMENTO
    # -----------------------------
    {
        "pergunta": "Quais formas de pagamento vocês aceitam?",
        "resposta": "Aceitamos Pix, cartão de crédito e débito."
    },
    {
        "pergunta": "Posso pagar na entrega?",
        "resposta": "No momento não. Todos os pedidos são pagos antecipadamente pelo site."
    },

    # -----------------------------
    # ENTREGA / FRETE
    # -----------------------------
    {
        "pergunta": "Vocês entregam em toda a cidade?",
        "resposta": "Sim! Fazemos entregas em toda a cidade de Campinas e região."
    },
    {
        "pergunta": "Qual o valor do frete?",
        "resposta": "O frete varia conforme a região. Acima de R$ 200, a entrega é gratuita!"
    },
    {
        "pergunta": "Vocês têm entrega grátis?",
        "resposta": "Sim! A entrega é gratuita em compras acima de R$ 200."
    },
    {
        "pergunta": "Como acompanho minha entrega?",
        "resposta": "Após a confirmação, você recebe um e-mail com o status e o código de acompanhamento."
    },
    {
        "pergunta": "Posso agendar o horário da entrega?",
        "resposta": "Sim! Durante o checkout, você pode selecionar o horário desejado."
    },

    # -----------------------------
    # HORÁRIO
    # -----------------------------
    {
        "pergunta": "Qual é o horário de funcionamento?",
        "resposta": "Funcionamos todos os dias das 8h às 19h."
    },
    {
        "pergunta": "Vocês abrem aos finais de semana?",
        "resposta": "Sim! Atendemos normalmente aos finais de semana e feriados."
    },

    # -----------------------------
    # RETIRADA
    # -----------------------------
    {
        "pergunta": "Posso retirar no local?",
        "resposta": "Pode sim! Basta selecionar a opção 'Retirar na loja' ao finalizar o pedido."
    },

    # -----------------------------
    # PRODUTOS
    # -----------------------------
    {
        "pergunta": "Quais sabores de bolo vocês têm?",
        "resposta": "Trabalhamos com chocolate, ninho, morango, prestígio, crocante, limão, maracujá e sabores especiais sob encomenda."
    },
    {
        "pergunta": "Os bolos são feitos no mesmo dia?",
        "resposta": "Sim! Produzimos tudo diariamente para garantir frescor e qualidade."
    },
    {
        "pergunta": "Qual a validade dos produtos?",
        "resposta": "Nossos bolos duram até 3 dias refrigerados. Produtos com frutas frescas duram até 2 dias."
    },

    # -----------------------------
    # ENCOMENDAS / URGÊNCIA
    # -----------------------------
    {
        "pergunta": "Consigo pedir um bolo para hoje?",
        "resposta": "Temos bolos prontos no dia! Para personalizados, depende da disponibilidade."
    },
    {
        "pergunta": "Aceitam encomenda de última hora?",
        "resposta": "Fazemos o possível para ajudar! Consulte a disponibilidade no chat."
    },

    # -----------------------------
    # SUPORTE
    # -----------------------------
    {
        "pergunta": "Como entro em contato com vocês?",
        "resposta": "Você pode enviar mensagem pela aba de contato ou pelo WhatsApp disponível no site."
    },
    {
        "pergunta": "Meu pedido atrasou, o que faço?",
        "resposta": "Pedimos desculpas! Entre em contato pelo chat com o número do seu pedido e resolvemos na hora."
    }
]

@faq_bp.route("/faq")
def faq():
    return render_template("faq.html", perguntas=faq_perguntas)
