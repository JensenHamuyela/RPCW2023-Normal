const express = require('express');
const bodyParser = require('body-parser');
const mongoose = require('mongoose');
//const mongoose = require('mongodb');

// Conectar ao banco de dados MongoDB
mongoose.connect('mongodb://localhost:27017', 
{ useNewUrlParser: true, useUnifiedTopology: true });

// Criar a aplicação Express
const app = express();
app.use(bodyParser.json());

//require('./db'); // Importar o arquivo db.js

// Verificar o estado da conexão
const db = mongoose.connection;
db.on('error', console.error.bind(console, 'Erro de conexão com o MongoDB:'));
db.once('open', () => {
  console.log('Conexão com o MongoDB estabelecida.');
});


// Rota: GET /contracts
app.get('/contracts', async (req, res) => {
  try {
    const contracts = await Contract.find();
    res.json(contracts);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
});

// Rota: GET /contracts/:id
app.get('/contracts/:id', getContract, (req, res) => {
  res.json(res.contract);
});

// Rota: GET /contracts?year=YYYY
app.get('/contracts', async (req, res) => {
  const year = req.query.year;
  try {
    const contracts = await Contract.find({ year: year });
    res.json(contracts);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
});

// Rota: GET /contracts?inst=AAA
app.get('/contracts', async (req, res) => {
  const institution = req.query.inst;
  try {
    const contracts = await Contract.find({ institution: institution });
    res.json(contracts);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
});

// Rota: GET /contracts/courses
app.get('/contracts/courses', async (req, res) => {
  try {
    const courses = await Contract.distinct('course');
    res.json(courses);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
});

// Rota: GET /contracts/institutions
app.get('/contracts/institutions', async (req, res) => {
  try {
    const institutions = await Contract.distinct('institution');
    res.json(institutions);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
});

// Rota: POST /contracts
app.post('/contracts', async (req, res) => {
  const contract = new Contract({
    year: req.body.year,
    institution: req.body.institution,
    course: req.body.course
    // Adicione aqui os outros campos do contrato
  });

  try {
    const newContract = await contract.save();
    res.status(201).json(newContract);
  } catch (err) {
    res.status(400).json({ message: err.message });
  }
});

// Rota: DELETE /contracts/:id
app.delete('/contracts/:id', getContract, async (req, res) => {
  try {
    await res.contract.remove();
    res.json({ message: 'Contrato removido com sucesso' });
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
});

// Função de middleware para obter um contrato pelo ID
async function getContract(req, res, next) {
  try {
    const contract = await Contract.findById(req.params.id);
    if (contract == null) {
      return res.status(404).json({ message: 'Contrato não encontrado' });
    }
    res.contract = contract;
    next();
  } catch (err) {
    return res.status(500).json({ message: err.message });
  }
}

// Iniciar o servidor na porta 15015
app.listen(15015, () => {
  console.log('Servidor iniciado na porta 15015');
});
