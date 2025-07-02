-- Script para inserir dados de teste no banco de dados

-- Inserir culturas
INSERT INTO culturas (nome, descricao) VALUES
('Soja', 'Cultura de soja'),
('Milho', 'Cultura de milho'),
('Arroz', 'Cultura de arroz'),
('Feijão', 'Cultura de feijão'),
('Trigo', 'Cultura de trigo'),
('Café', 'Cultura de café'),
('Cana-de-açúcar', 'Cultura de cana-de-açúcar'),
('Algodão', 'Cultura de algodão')
ON CONFLICT (nome) DO NOTHING;

-- Inserir produtores
INSERT INTO produtores (cpf_cnpj, nome) VALUES
('123.456.789-01', 'João Silva'),
('987.654.321-02', 'Maria Santos'),
('456.789.123-03', 'Pedro Oliveira'),
('789.123.456-04', 'Ana Costa'),
('321.654.987-05', 'Carlos Ferreira'),
('654.987.321-06', 'Lucia Pereira'),
('147.258.369-07', 'Roberto Lima'),
('258.369.147-08', 'Fernanda Souza'),
('369.147.258-09', 'Marcos Alves'),
('951.753.852-10', 'Juliana Martins')
ON CONFLICT (cpf_cnpj) DO NOTHING;

-- Inserir propriedades
INSERT INTO propriedades (nome, estado, municipio, area_total, area_agricultavel, area_vegetacao, produtor_id) VALUES
('Fazenda São João', 'SP', 'Campinas', 1500.0, 1200.0, 300.0, (SELECT id FROM produtores WHERE cpf_cnpj = '123.456.789-01')),
('Sítio Boa Vista', 'MG', 'Uberlândia', 800.0, 600.0, 200.0, (SELECT id FROM produtores WHERE cpf_cnpj = '987.654.321-02')),
('Rancho Alegre', 'GO', 'Goiânia', 2000.0, 1600.0, 400.0, (SELECT id FROM produtores WHERE cpf_cnpj = '456.789.123-03')),
('Fazenda Santa Clara', 'PR', 'Londrina', 1200.0, 900.0, 300.0, (SELECT id FROM produtores WHERE cpf_cnpj = '789.123.456-04')),
('Sítio Primavera', 'RS', 'Porto Alegre', 600.0, 450.0, 150.0, (SELECT id FROM produtores WHERE cpf_cnpj = '321.654.987-05')),
('Fazenda Nova Esperança', 'MT', 'Cuiabá', 3000.0, 2400.0, 600.0, (SELECT id FROM produtores WHERE cpf_cnpj = '654.987.321-06')),
('Rancho São Pedro', 'MS', 'Campo Grande', 1800.0, 1400.0, 400.0, (SELECT id FROM produtores WHERE cpf_cnpj = '147.258.369-07')),
('Fazenda Bela Vista', 'BA', 'Salvador', 900.0, 700.0, 200.0, (SELECT id FROM produtores WHERE cpf_cnpj = '258.369.147-08')),
('Sítio dos Ipês', 'TO', 'Palmas', 2500.0, 2000.0, 500.0, (SELECT id FROM produtores WHERE cpf_cnpj = '369.147.258-09')),
('Fazenda Progresso', 'PA', 'Belém', 3500.0, 2800.0, 700.0, (SELECT id FROM produtores WHERE cpf_cnpj = '951.753.852-10'))
ON CONFLICT (nome) DO NOTHING;

-- Inserir safras
INSERT INTO safras (ano, descricao, propriedade_id, cultura_id) VALUES
(2023, 'Safra 2023/2024', (SELECT id FROM propriedades WHERE nome = 'Fazenda São João'), (SELECT id FROM culturas WHERE nome = 'Soja')),
(2023, 'Safra 2023/2024', (SELECT id FROM propriedades WHERE nome = 'Sítio Boa Vista'), (SELECT id FROM culturas WHERE nome = 'Milho')),
(2023, 'Safra 2023/2024', (SELECT id FROM propriedades WHERE nome = 'Rancho Alegre'), (SELECT id FROM culturas WHERE nome = 'Arroz')),
(2023, 'Safra 2023/2024', (SELECT id FROM propriedades WHERE nome = 'Fazenda Santa Clara'), (SELECT id FROM culturas WHERE nome = 'Feijão')),
(2023, 'Safra 2023/2024', (SELECT id FROM propriedades WHERE nome = 'Sítio Primavera'), (SELECT id FROM culturas WHERE nome = 'Trigo')),
(2024, 'Safra 2024/2025', (SELECT id FROM propriedades WHERE nome = 'Fazenda Nova Esperança'), (SELECT id FROM culturas WHERE nome = 'Café')),
(2024, 'Safra 2024/2025', (SELECT id FROM propriedades WHERE nome = 'Rancho São Pedro'), (SELECT id FROM culturas WHERE nome = 'Cana-de-açúcar')),
(2024, 'Safra 2024/2025', (SELECT id FROM propriedades WHERE nome = 'Fazenda Bela Vista'), (SELECT id FROM culturas WHERE nome = 'Algodão')),
(2024, 'Safra 2024/2025', (SELECT id FROM propriedades WHERE nome = 'Sítio dos Ipês'), (SELECT id FROM culturas WHERE nome = 'Soja')),
(2024, 'Safra 2024/2025', (SELECT id FROM propriedades WHERE nome = 'Fazenda Progresso'), (SELECT id FROM culturas WHERE nome = 'Milho'))
ON CONFLICT DO NOTHING;