public class Nigromante extends Personaje implements Hechicero {

    private int mana;
    private int almasAbsorbidas;

    public Nigromante(String nombre, int nivel, int puntosVida,
                      int mana, int almasAbsorbidas) {
        super(nombre, nivel, puntosVida);
        this.mana = mana;
        this.almasAbsorbidas = almasAbsorbidas;
    }

    @Override
    public void atacar() throws RpgException {
        // 1. Verifica que esté vivo -> lanza PersonajeDerrotadoException
        if (!isEstaVivo()) {
            throw new PersonajeDerrotadoException(getNombre());
        }

        // 2. Verifica que tenga mana >= 15 -> lanza RecursoInsuficienteException("mana", mana)
        if (mana < 15) {
            throw new RecursoInsuficienteException("mana", mana);
        }

        // 3. Si pasa, resta 15 al mana y ejecuta el ataque
        mana -= 15;
        System.out.println("[" + nombre + "] drena la esencia vital e invoca sombras.");
    }

    @Override
    public int calcularDanio() {
        int danioBase = nivel * 25;
        int bonusMana = mana / 2;
        int bonusAlmas = almasAbsorbidas * 15;
        return danioBase + bonusMana + bonusAlmas;
    }

    @Override
    public void lanzarHechizo() {
        System.out.println(nombre + " lanza: ¡Maldición de decadencia! (maná: " + mana + ")");
    }

    @Override
    public int getMana() {
        return mana;
    }

    public int getAlmasAbsorbidas() {
        return almasAbsorbidas;
    }

    @Override
    public String toString() {
        return super.toString() + " | Maná: " + mana + " | Almas: " + almasAbsorbidas;
    }
}
