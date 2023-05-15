from numpy import datetime_as_string
import requests
import json
import datetime

url = "url"


headers = {
  'Content-Type': 'text/xml; charset=utf-8',
  'SOAPAction': 'http://tempuri.org/'
}

contador = 0

cnpjs = ['cnpj']


for cnpj in cnpjs:
  for ano in range(2020, 2023):
    for mes in range(1, 13):
      payload = "<soapenv:Envelope xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\" xmlns:sch=\"http://www.ans.gov.br/padroes/tiss/schemas\" xmlns:xd=\"http://www.w3.org/2000/09/xmldsig#\">\n   <soapenv:Header/>\n   <soapenv:Body>\n      <sch:solicitacaoDemonstrativoRetornoWS>\n         <sch:cabecalho>\n            <sch:identificacaoTransacao>\n               <sch:tipoTransacao>DEMONSTRATIVO_PAGAMENTO</sch:tipoTransacao>\n               <sch:sequencialTransacao>teste</sch:sequencialTransacao>\n               <sch:dataRegistroTransacao>2022-09-22</sch:dataRegistroTransacao>\n               <sch:horaRegistroTransacao>18:18:00</sch:horaRegistroTransacao>\n            </sch:identificacaoTransacao>\n            <!--Optional:-->\n            <sch:falhaNegocio></sch:falhaNegocio>\n            <sch:origem>\n            <sch:identificacaoPrestador>\n                <sch:CNPJ>"+ cnpj +"</sch:CNPJ>\n            </sch:identificacaoPrestador>\n            </sch:origem>\n            <sch:destino>\n               <sch:registroANS>421669</sch:registroANS>\n            </sch:destino>\n            <sch:Padrao>3.05.00</sch:Padrao>\n         </sch:cabecalho>\n         <sch:solicitacaoDemonstrativoRetorno>\n            <!--You have a CHOICE of the next 2 items at this level-->\n            <sch:demonstrativoPagamento>\n               <sch:dadosPrestador>\n                  <!--You have a CHOICE of the next 3 items at this level-->\n                  <sch:codigoPrestadorNaOperadora>000019</sch:codigoPrestadorNaOperadora>\n                  <sch:nomeContratado>UNIDADE REFERENCIADA OSWALDO CRUZ VERGUEIRO</sch:nomeContratado>\n               </sch:dadosPrestador>\n               <sch:dataSolicitacao>2022-09-22</sch:dataSolicitacao>\n               <sch:tipoDemonstrativo>1</sch:tipoDemonstrativo>\n               <sch:periodo>\n                  <!--You have a CHOICE of the next 2 items at this level-->\n                  <sch:competencia>"+ str(ano) + str(mes).zfill(2) +"</sch:competencia>\n               </sch:periodo>\n            </sch:demonstrativoPagamento>\n         </sch:solicitacaoDemonstrativoRetorno>\n         <sch:hash>?</sch:hash>\n         <!--Optional:-->\n      </sch:solicitacaoDemonstrativoRetornoWS>\n   </soapenv:Body>\n</soapenv:Envelope>"
      response = requests.request("POST", url, headers=headers, data=payload)

      print('processando ' + cnpj + 'competencia '+ str(ano) + str(mes).zfill(2))
      competencia = str(ano) + str(mes).zfill(2)

      with open('HAOC_PAGAMENTO/'+ str(ano) +'/' + str(mes).zfill(2) + '/' + 'CNPJ_' + cnpj + competencia + '.xml', 'w', encoding="utf-8") as fw:
        if not response.text.__contains__('SEM NENHUMA OCORRENCIA DE MOVIMENTO NA COMPETENCIA'):
          fw.write(response.text)