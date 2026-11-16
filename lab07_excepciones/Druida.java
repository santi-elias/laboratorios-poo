public class Druida extends Personaje implements Hechicero, Sanador {

    private int mana;
    private int poderCuracion;
    private String formaAnimal;

    public Druida(String nombre, int nivel, int puntosVida,
                  int mana, int poderCuracion, String formaAnimal) {
        super(nombre, nivel, puntosVida);
        this.mana = mana;
        this.poderCuracion = poderCuracion;
        this.formaAnimal = formaAnimal;
    }

    @Override
    public void atacar() throws RpgException {
        // 1. Verifica que esté vivo -> lanza PersonajeDerrotadoException
        if (!isEstaVivo()) {
            throw new PersonajeDerrotadoException(getNombre());
        }

        // 2. Verifica que tenga mana >= 10 -> lanza RecursoInsuficienteException("mana", mana)
        if (mana < 10) {
            throw new RecursoInsuficienteException("mana", mana);
        }

        // 3. Resta 10 al mana y ejecuta el ataque normal
        mana -= 10;
        System.out.println("[" + nombre + "] invoca raíces del bosque y ataca con furia natural.");
    }

    @Override
    public int calcularDanio() {
        int danioBase = nivel * 20;
        int bonusMana = mana / 2;
        int bonusForma = "Oso".equalsIgnoreCase(formaAnimal) ? 40 : 20;
        return danioBase + bonusMana + bonusForma;
    }

    @Override
    public void lanzarHechizo() {
        System.out.println(nombre + " lanza: ¡Tormenta de espinas! (maná: " + mana + ")");
    }

    @Override
    public int getMana() {
        return mana;
    }

    @Override
    public void curarAliado(Personaje aliado) throws RpgException {
        // 1. Verifica que aliado no sea null -> lanza PersonajeNuloException("curarAliado")
        if (aliado == null) {
            throw new PersonajeNuloException("curarAliado");
        }

        // 2. Verifica que el aliado esté vivo -> lanza AccionInvalidaException("curarAliado", "No se puede curar a un personaje derrotado")
        if (!aliado.isEstaVivo()) {
            throw new AccionInvalidaException("curarAliado", "No se puede curar a un personaje derrotado");
        }

        // 3. Cura normalmente
        aliado.puntosVida += poderCuracion;
        System.out.println(nombre + " toca la tierra y cura a " + aliado.getNombre() +
                           " +" + poderCuracion + ". Vida: " + aliado.getPuntosVida());
    }

    @Override
    public int getPoderCuracion() {
        return poderCuracion;
    }

    public String getFormaAnimal() {
        return formaAnimal;
    }

    @Override
    public String toString() {
        return super.toString() + " | Maná: " + mana + " | Forma Animal: " + formaAnimal;
    }
}
