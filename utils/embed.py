from discord import Embed
from nekos import img
COR = 0xF26DDC

def embedajuda(membro):
    ajuda=Embed(
        title="Ajuda! <a:blush1:592371658589732874>",
        description=f"Olá {membro}, me chamo Raphtalia e sou um simples bot para discord feito pelo <@!207947146371006464>!",
        color=COR)
    ajuda.set_footer(text="Siga-me no twitter: http://twitter.com/KKKBini.")
    ajuda.add_field(name="Precisa de ajuda? <:raphYamero:674648257489797140>", value='Veja minha lista de comandos:\nhttp://raphtalia.kody.mobi', inline=True)
    ajuda.add_field(name="Precisa de ajuda específica? <:raphNhom:674648257321893940>", value='Entre no meu Discord!\nhttps://discord.gg/df7XWzt', inline=True)
    ajuda.add_field(name="Quer conhecer meu código? <:raphHm:674462160876732448>", value='Acesse minha página do github!\nhttp://github.com/losty17/raphtalia', inline=True)

    ajuda.set_image(url='https://coverfiles.alphacoders.com/765/76564.png')
    return ajuda

def embedwelcome(member, bot, prefix):
    welcomeembed = Embed(
        title='Tragam as bebidas!', 
        description=f'{member.mention} acabou de chegar!', 
        color=COR)
    welcomeembed.add_field(
        name="<:raphNhom:674648257321893940> Precisa de ajuda?", 
        value=f'Use o comando `{prefix}ajuda` para acessar meu painel de ajuda!', 
        inline=True)
    welcomeembed.add_field(
        name="<:raphOh:674648256608731176> Siga meu criador nas redes sociais!", 
        value=f'Use o comando `{prefix}author` para receber um link direto.', 
        inline=True)
    welcomeembed.add_field(
        name="<:raphPat:674648256529170438> Quer divulgar meu servidor?", 
        value=f'Digite discord para receber o link de convite para meu servidor!', 
        inline=True)
    welcomeembed.set_image(url='https://66.media.tumblr.com/d42fbc38b77d5e93f0dabd666d6fe5aa/tumblr_plyo8ka1yZ1y5sd79o3_500.png')
    welcomeembed.set_author(name=f'{bot.user}', icon_url=bot.user.avatar_url)
    #welcomeembed.set_footer(text=f'A {member.guild.name} agora possui {member.guild.size}')
    return welcomeembed

def neko_img_text(image, title='', title2=""):
    emb = Embed(title=f'{title} {title2}', colour=0xF26DDC)
    emb.set_image(url=img(image))
    emb.set_footer(text=f'Busca feita com o termo: "{image}"')
    return emb