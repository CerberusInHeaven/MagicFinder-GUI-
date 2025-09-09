import { PrismaClient } from '@prisma/client'
import { Router, Request } from 'express'
import { z } from 'zod'
import { verificaToken } from '../middlewares/verificaToken'

const prisma = new PrismaClient()
const router = Router()

const bugigangasSchema = z.object({
    nome: z.string(),
    descricao: z.string(),
    Classe: z.string()
})

router.get("/", async (req, res) => {
  try {
    const bugigangas = await prisma.bugigangas.findMany({  
      orderBy: { id: 'desc' },
      select: {
        id: true,
        nome: true,
        descricao: true,
        Classe: true,  
        usuario: true
      }
    })
    res.status(200).json(bugigangas)
  } catch (error) {
    res.status(500).json({erro: error})
  }
})

interface CustomRequest extends Request {
  userLogadoId?: number;
}

router.post("/", verificaToken, async (req: CustomRequest, res) => {
  const valida = bugigangasSchema.safeParse(req.body)
  if (!valida.success) {
    res.status(400).json({ erro: valida.error })
    return
  }

  try {
    const bugiganga = await prisma.bugigangas.create({  
      data: {
        ...valida.data,
        usuario: {
          connect: { id: req.userLogadoId }
        }
      }
    })
    res.status(201).json(bugiganga)
  } catch (error) {
    res.status(400).json({ error })
  }
})

router.delete("/:id", verificaToken, async (req: any, res) => {
  const { id } = req.params

  try {
    const bugiganga = await prisma.bugigangas.delete({  
      where: { id: Number(id) }
    })

    await prisma.log.create({
      data: { 
        descricao: `Exclusão da bugiganga: ${id}`, 
        complemento: `Funcionário: ${req.userLogadoNome}`,
        usuarioId: req.userLogadoId,
        acao: 'deletar_bugiganga',  
      }
    })

    res.status(200).json(bugiganga)
  } catch (error) {
    res.status(400).json({ erro: error })
  }
})

router.put("/:id", verificaToken, async (req, res) => {
  const { id } = req.params

  const valida = bugigangasSchema.safeParse(req.body)
  if (!valida.success) {
    res.status(400).json({ erro: valida.error })
    return
  }

  try {
    const bugiganga = await prisma.bugigangas.update({  
      where: { id: Number(id) },
      data: valida.data
    })
    res.status(201).json(bugiganga)
  } catch (error) {
    res.status(400).json({ error })
  }
})

router.patch("/:id", async (req, res) => {
  const { id } = req.params

  const partialBugigangasSchema = bugigangasSchema.partial()
  const valida = partialBugigangasSchema.safeParse(req.body)
  if (!valida.success) {
    res.status(400).json({ erro: valida.error })
    return
  }

  try {
    const bugiganga = await prisma.bugigangas.update({  
      where: { id: Number(id) },
      data: valida.data
    })
    res.status(201).json(bugiganga)
  } catch (error) {
    res.status(400).json({ error })
  }
})

export default router