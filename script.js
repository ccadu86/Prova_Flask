document.addEventListener('DOMContentLoaded', () => {
  fetchData();
});

const fetchData = async () => {
  try {
    const response = await axios.get('http://localhost:5000/read');
    const recordsList = document.getElementById('recordsList');
    recordsList.innerHTML = '';

    response.data.forEach((item) => {
      const li = document.createElement('li');
      li.innerHTML = `${item.Nome}, ${item.Idade} anos, ${item.Cidade} <button onclick="deleteRecord('${item.ID}')">Excluir</button> <button onclick="openUpdateModal('${item.ID}', '${item.Nome}', '${item.Idade}', '${item.Cidade}')">Editar</button>`;
      recordsList.appendChild(li);
    });
  } catch (error) {
    console.error('Erro ao buscar dados:', error);
  }
};

const createRecord = async () => {
  const inputNome = document.getElementById('inputNome').value;
  const inputIdade = document.getElementById('inputIdade').value;
  const inputCidade = document.getElementById('inputCidade').value;

  if (!inputNome || !inputIdade || !inputCidade) {
    alert('Preencha todos os campos!');
    return;
  }

  try {
    await axios.post('http://localhost:5000/create', { Nome: inputNome, Idade: inputIdade, Cidade: inputCidade });
    alert('Registro criado com sucesso!');
    fetchData();
  } catch (error) {
    console.error('Erro ao criar registro:', error);
  }
};

const deleteRecord = async (id) => {
  try {
    await axios.delete(`http://localhost:5000/delete/${id}`);
    fetchData();
  } catch (error) {
    console.error('Erro ao deletar registro:', error);
  }
};

const openUpdateModal = (id, nome, idade, cidade) => {
  const updatedNome = prompt('Digite o novo nome:', nome);
  const updatedIdade = prompt('Digite a nova idade:', idade);
  const updatedCidade = prompt('Digite a nova cidade:', cidade);

  if (updatedNome !== null && updatedIdade !== null && updatedCidade !== null) {
    updateRecord(id, updatedNome, updatedIdade, updatedCidade);
  }
};

const updateRecord = async (id, updatedNome, updatedIdade, updatedCidade) => {
  try {
    await axios.put(`http://localhost:5000/update/${id}`, { Nome: updatedNome, Idade: updatedIdade, Cidade: updatedCidade });
    fetchData();
  } catch (error) {
    console.error('Erro ao atualizar registro:', error);
  }
};
