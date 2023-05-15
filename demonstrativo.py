from numpy import datetime_as_string
import requests
import json
import datetime

url = "url"

cnpj = ''
cod_rda = ''
nom_rda = ''
protocolo = ''
protocolos = ''
ano = ''
mes = ''
ano_anterior = ''
mes_anterior = ''

headers = {
  'Content-Type': 'text/xml; charset=utf-8',
  'SOAPAction': 'http://tempuri.org/'
}



f = open('entrada.json')
data = json.load(f)

contador = 0

for i in data:
  cnpj = i['CNPJ']
  cod_rda = i['BCI_CODRDA']
  nom_rda = i['NOM_RDA']
  ano = i['BCI_ANO']
  mes = i['BCI_MES']    
  protocolos = "<sch:numeroProtocolo>" + i['BCI_CODPEG'] +"</sch:numeroProtocolo>\n"
  payload = "<soapenv:Envelope xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\" xmlns:sch=\"http://www.ans.gov.br/padroes/tiss/schemas\" xmlns:xd=\"http://www.w3.org/2000/09/xmldsig#\">\n   <soapenv:Header/>\n   <soapenv:Body>\n      <sch:solicitacaoDemonstrativoRetornoWS>\n         <sch:cabecalho>\n            <sch:identificacaoTransacao>\n               <sch:tipoTransacao>DEMONSTRATIVO_PAGAMENTO</sch:tipoTransacao>\n               <sch:sequencialTransacao>20220906</sch:sequencialTransacao>\n               <sch:dataRegistroTransacao>2022-09-11</sch:dataRegistroTransacao>\n               <sch:horaRegistroTransacao>18:18:00</sch:horaRegistroTransacao>\n            </sch:identificacaoTransacao>\n            <!--Optional:-->\n            <sch:falhaNegocio></sch:falhaNegocio>\n            <sch:origem>\n\t\t\t<sch:identificacaoPrestador>\n\t\t\t\t<sch:CNPJ>" + cnpj + "</sch:CNPJ>\n\t\t\t</sch:identificacaoPrestador>\n            </sch:origem>\n            <sch:destino>\n               <sch:registroANS>421669</sch:registroANS>\n            </sch:destino>\n            <sch:Padrao>3.05.00</sch:Padrao>\n         </sch:cabecalho>\n         <sch:solicitacaoDemonstrativoRetorno>\n            <sch:demonstrativoAnalise>\n               <sch:dadosPrestador>\n                  <!--You have a CHOICE of the next 3 items at this level-->\n                  <sch:codigoPrestadorNaOperadora>"+ cod_rda +"</sch:codigoPrestadorNaOperadora>\n                  <sch:nomeContratado>"+ nom_rda +"</sch:nomeContratado>\n               </sch:dadosPrestador>\n               <sch:dataSolicitacao>2022-09-11</sch:dataSolicitacao>\n               <sch:protocolos>\n                  <!--1 to 30 repetitions:-->\n                  "+ protocolos +"\n               </sch:protocolos>\n            </sch:demonstrativoAnalise>\n         </sch:solicitacaoDemonstrativoRetorno>\n         <sch:hash></sch:hash>\n         <!--Optional:-->\n      </sch:solicitacaoDemonstrativoRetornoWS>\n   </soapenv:Body>\n</soapenv:Envelope>"
  response = requests.request("POST", url, headers=headers, data=payload)

  print('processando ' + str(contador) + ' de ' + str(len(data)))

  with open('HAOC/'+ ano +'/' + mes + '/' + 'RDA_' + i['BCI_CODRDA'] +'PEG_' + i['BCI_CODPEG'] + '.xml', 'w', encoding="utf-8") as fw:
    fw.write(response.text)
  contador = contador + 1