const express = require('express');
const app = express();
const port = 15016;

// Configurar cabeçalho com metainformações
app.use((req, res, next) => {
  res.set('Content-Type', 'text/html');
  res.set('X-Powered-By', 'My Service');
  next();
});

// Rota para página principal
app.get('http://localhost:15016', (req, res) => {
  // Obter lista de contratos da API
  const contratos = obterContratos();

  // Criar tabela HTML com a lista de contratos
  let tabela = '<table>';
  tabela += '<thead><tr><th>ID</th><th>Data Início</th><th>Data Fim</th><th>Instituição</th><th>Áreas de Investigação</th></tr></thead>';
  tabela += '<tbody>';
  contratos.forEach((contrato) => {
    tabela += '<tr>';
    tabela += `<td><a href="/{contrato._id}">{contrato._id}</a></td>`;
    tabela += `<td>{contrato.DataInicioContrato}</td>`;
    tabela += `<td>{contrato.DataFimContrato}</td>`;
    tabela += `<td><a href="/instituicao/{contrato.NomeInstituicao}">{contrato.NomeInstituicao}</a></td>`;
    tabela += `<td>{contrato.AreasInvestigacao}</td>`;
    tabela += '</tr>';
  });
  tabela += '</tbody>';
  tabela += '</table>';

  // Enviar página HTML com a tabela de contratos
  res.send(`
    <html>
      <head>
        <title>Lista de Contratos</title>
      </head>
      <body>
        <h1>Lista de Contratos</h1>
        {tabela}
      </body>
    </html>
  `);
});

// Rota para página do contrato
app.get('http://localhost:15016/:id', (req, res) => {
  const id = req.params.id;

// Rota para página NIPCInstituicao
app.get('http://localhost:15016/:nipc', (req, res) => {
  const id = req.params.id;


  // Obter contrato da API
  const contrato = obterContratoPorId(id);
  if (!contrato) {
    res.status(404).send('Contrato não encontrado');
    return;
  }

  // Criar página HTML com os dados do contrato
  res.send(`
    <html>
      <head>
        <title>{contrato._id}</title>
      </head>
      <body>
        <h1>{contrato._id}</h1>
        <p>Data Início: {contrato.DataInicioContrato}</p>
        <p>Data Fim: {contrato.DataFimContrato}</p>
        <p>Instituição: <a href="/instituicao/${contrato.NomeInstituicao}">{contrato.NomeInstituicao}</a></p>
        <p>Áreas de Investigação: {contrato.AreasInvestigacao}</p>
        <a href="/">Voltar à página principal</a>
      </
