import express from 'express'
import routesUsuarios from './routes/usuarios'
import routesLogin from './routes/login'
import routesbugi from './routes/bugigangas'

const app = express()
const port = 3000

app.use(express.json())

app.use('/usuarios', routesUsuarios)
app.use('/login', routesLogin)
app.use('/bugigangas', routesbugi)

app.get('/', (req, res) => {    
    res.send('BUGIGANGAS CIA')
})

app.listen(port, () => {
    console.log(`O PORTAL DE BUGIGAS ESTA RODANDO EM: ${port}`)
})