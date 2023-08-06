# oeispy
Simple Python library for OEIS ( Online Encyclopedia of Integer Sequences )

List of methods with examples :

Query OEIS
```sh
import oeispy as op
res=op.resultEois('1,9,15,19')
```
Best Result
```sh
op.topResult(res)
```
Count Results
```sh
op.countResult(res)
```
Get Number
```sh
op.getNumber(res[0])
```
Get Id
```sh
op.getId(res[0])
```
Get Data
```sh
op.getData(res[0])
```
Get Name
```sh
op.getName(res[0])
```
Get Comment
```sh
op.getComment(res[0])
```
Get Link
```sh
op.getLink(res[0])
```
Get Example
```sh
op.getExample(res[0])
```
Similarly , getAuthor(..), getTime(..), getCreated(..), getFormula(..), getProgram(..)

Get Graph and Save Image
```sh
op.getGraph('A000001')
```
Get Random
```sh
res=op.getRandom()
```





