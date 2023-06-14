'''SISTEMA DE GERENCIAMENTO DE PRODUTO'''

class Produto:
    def __init__(self, descricao: str, quantidade: int, precoCompra: float, precoVenda: float):
        self.descricao = descricao
        self.quantidade = quantidade
        self.precoCompra = precoCompra
        self.precoVenda = precoVenda
        self.percentualLucro = self.calculoPercentualLucro()

    def calculoPercentualLucro(self):
        lucroTotal = (self.precoVenda - self.precoCompra)
        percentual = ((lucroTotal / self.precoCompra) * 100)
        return percentual

def cadastrarProduto():
    import mysql.connector
    mybd = mysql.connector.connect(
        host="127.0.0.1", user="root", password="rootfelipi", database="bancoAtividades"
    )
    mycurso = mybd.cursor()
    descricao = input("Descrição do produto: ")
    sqlConsulta = "SELECT codigo FROM produtos WHERE descricao = '" +descricao+ "' LIMIT 1"
    mycurso.execute(sqlConsulta)
    if (mycurso.rowcount > 0):
        print("Produto com a descrição informada já cadastrado.")
        mycurso.close()
        mybd.commit()
        mybd.close()
        return
    mycurso.reset()
    quantidade = int(input("Quantidade em estoque: "))
    precoCompra = float(input("Preço de compra do produto: "))
    precoVenda = float(input("Preço de venda do produto: "))
    produto = Produto(descricao, quantidade, precoCompra, precoVenda)
    sql = "INSERT INTO produtos (descricao, quantidade, precoCompra, precoVenda, percentualLucro) VALUES (%s, %s, %s, %s, %s)"
    dados = (produto.descricao, produto.quantidade, produto.precoCompra, produto.precoVenda, produto.percentualLucro)
    mycurso.execute(sql, dados)
    if (mycurso.rowcount >= 1):
        print("Produto cadastrado com sucesso. ")
    mycurso.close()
    mybd.commit()
    mybd.close()

def excluirProduto():
    import mysql.connector
    mybd = mysql.connector.connect(
        host="127.0.0.1", user="root", password="rootfelipi", database="bancoAtividades"
    )
    mycurso = mybd.cursor()
    sqlConsulta = "SELECT codigo, descricao FROM produtos ORDER BY codigo"
    mycurso.execute(sqlConsulta)
    resultado = mycurso.fetchall()
    if (mycurso.rowcount >=1 ):
        for registro in resultado:
            print("Id do produto = ", registro[0], "Descrição = ", registro[1])
    else:
        print("Não existe produtos cadastrados para exclusão.")
        mycurso.close()
        mybd.commit()
        mybd.close()
        return
    codigoProduto = int(input("Código do produto: "))
    sql = "DELETE FROM produtos WHERE codigo = " + str(codigoProduto)
    mycurso.execute(sql)
    if (mycurso.rowcount >= 1):
        print("Produto excluido com sucesso. ")
    mycurso.close()
    mybd.commit()
    mybd.close()

def alterarProduto():
    import mysql.connector
    mybd = mysql.connector.connect(
        host="127.0.0.1", user="root", password="rootfelipi", database="bancoAtividades"
    )
    mycurso = mybd.cursor()
    sqlConsulta = "SELECT codigo, descricao FROM produtos ORDER BY codigo"
    mycurso.execute(sqlConsulta)
    resultado = mycurso.fetchall()
    if (mycurso.rowcount >=1 ):
        for registro in resultado:
            print("Id do produto = ", registro[0], "Descrição = ", registro[1])
    else:
        print("Não existe produtos cadastrados para realizar uma alteração.")
        mycurso.close()
        mybd.commit()
        mybd.close()
        return
    codigoProduto = int(input("Código do produto: "))
    print("Digite as novas informações referente ao produto.")
    descricao = input("Descrição: ")
    quantidade = input("Quantidade: ")
    precoCompra = float(input("Preço compra: "))
    precoVenda = float(input("Preço venda: "))
    produto = Produto(descricao, quantidade, precoCompra, precoVenda)
    sql = "UPDATE produtos SET descricao = %s, quantidade = %s, precoCompra = %s, precoVenda = %s, percentualLucro = %s WHERE codigo = %s"
    dados = (produto.descricao, produto.quantidade, produto.precoCompra, produto.precoVenda, produto.percentualLucro, codigoProduto)
    mycurso.execute(sql, dados)
    if (mycurso.rowcount >= 1):
        print("Produto alterado com sucesso. ")
    mycurso.close()
    mybd.commit()
    mybd.close()

def consultarProduto():
    import mysql.connector
    mybd = mysql.connector.connect(
        host="127.0.0.1", user="root", password="rootfelipi", database="bancoAtividades"
    )
    mycurso = mybd.cursor()
    print("Consultar unico produto ?")
    print("Sim = S    Não  =  N")
    tipoAcao = input("")
    if (tipoAcao == "s" or tipoAcao == "S"):
        codigoProduto = int(input("Código do produto: "))
        sqlConsulta = "SELECT codigo, descricao, quantidade, precoCompra, precoVenda, percentualLucro FROM produtos WHERE codigo = " + str(codigoProduto) + " ORDER BY codigo"
    else:
        sqlConsulta = "SELECT codigo, descricao, quantidade, precoCompra, precoVenda, percentualLucro FROM produtos ORDER BY codigo"
    mycurso.execute(sqlConsulta)
    resultado = mycurso.fetchall()
    if (mycurso.rowcount >=1 ):
        for registro in resultado:
            print("Id do produto = ", registro[0], "Descrição = ", registro[1], "Quantidade = ", registro[2], "Preço compra = ", registro[3], "Preço venda = ", registro[4], "Percentual de lucro = ", registro[5])
    else:
        print("Produto(s) não cadastrado(s).")
    mycurso.close()
    mybd.commit()
    mybd.close()

tipoAcao = ""
while tipoAcao != ("5") or tipoAcao != (5):
    print()
    print("Tipos de ações para realizar.")
    print("Cadastrar produto  =  1    Excluir produto  =  2    Alterar produto  =  3    Consultar produto  =  4    Finalizar programa  =  5")
    tipoAcao = input()
    if (tipoAcao == ("1") or tipoAcao == (1)):
        cadastrarProduto()
    elif (tipoAcao == ("2") or tipoAcao == (2)):
        excluirProduto()
    elif (tipoAcao == ("3") or tipoAcao == (3)):
        alterarProduto()
    elif (tipoAcao == ("4") or tipoAcao == (4)):
        consultarProduto()
    else:
        print("Finalizando operações")
        break