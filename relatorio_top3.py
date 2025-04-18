import psycopg2
import matplotlib.pyplot as plt
from fpdf import FPDF

# Conexão com o banco
conn = psycopg2.connect(
    dbname="cadastro_atletas",
    user="fabio",
    password="1234",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# Buscar todos os atletas
cursor.execute("""
    SELECT id, nome, idade, tempo_treino,
           categoria1, nota1, classificacao1,
           categoria2, nota2, classificacao2,
           categoria3, nota3, classificacao3,
           categoria4, nota4, classificacao4,
           categoria5, nota5, classificacao5
    FROM atletas
""")
atletas = cursor.fetchall()

# Função para calcular a média correta
def calcular_media(atleta):
    # Índices das notas no SELECT
    indices_notas = [5, 8, 11, 14, 17]
    notas = []

    for i in indices_notas:
        nota = atleta[i]
        if nota is not None:
            try:
                notas.append(float(nota))
            except ValueError:
                pass

    return sum(notas) / len(notas) if notas else 0

# Pegar os 3 atletas com maior média
atletas_ordenados = sorted(atletas, key=calcular_media, reverse=True)[:3]



# Criar gráfico de pizza com as médias
nomes = [a[1] for a in atletas_ordenados]
medias = [calcular_media(a) for a in atletas_ordenados]

colors = ['#ff9999', '#66b3ff', '#99ff99']

plt.figure(figsize=(5, 5))
plt.pie(medias, labels=nomes, autopct='%1.1f%%', startangle=140, colors=colors)
plt.title('Distribuição das Médias - Top 3 Atletas')
plt.tight_layout()
plt.savefig("grafico.png")
plt.close()

# Criar o PDF
pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()
pdf.set_font("Arial", "B", 16)
pdf.cell(0, 10, "Relatório - Top 3 Atletas", ln=True, align="C")
# Inserir gráfico no PDF
pdf.image("grafico.png", x=50, w=100)

pdf.ln(10)


for atleta in atletas_ordenados:
    media = calcular_media(atleta)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, f"Nome: {atleta[1]}", ln=True)
    pdf.set_font("Arial", "", 11)
    pdf.cell(0, 8, f"Idade: {atleta[2]}  |  Tempo de treino: {atleta[3]} anos", ln=True)
    pdf.cell(0, 8, f"Média de notas: {media:.2f}", ln=True)
    pdf.ln(2)

    for i in range(1, 6):
        base = 3 + (i - 1) * 3
        categoria = atleta[base + 1]
        nota = atleta[base + 2]
        classificacao = atleta[base + 3]

        if categoria:
            nota_fmt = f"{float(nota):.2f}" if nota is not None else "N/A"
            clas_fmt = classificacao if classificacao else "N/A"
            pdf.cell(0, 8, f"- {categoria} | Nota: {nota_fmt} | Classificação: {clas_fmt}", ln=True)

    pdf.ln(8)


  


# Salvar o PDF
pdf.output("top3_atletas.pdf")
print("✅ PDF gerado com sucesso: top3_atletas.pdf")
