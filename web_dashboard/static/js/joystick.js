const joystick = document.getElementById('joystick');
const container = document.getElementById('joystick-container');

container.addEventListener('mousedown', (event) => {
    const rect = container.getBoundingClientRect();

    const handleMouseMove = (e) => {
        const centerX = rect.left + rect.width / 2;
        const centerY = rect.top + rect.height / 2;
        const maxRadius = rect.width / 2;

        let x = e.clientX - centerX;
        let y = e.clientY - centerY;

        // limite au cercle
        const distance = Math.sqrt(x * x + y * y);
        if (distance > maxRadius) {
            const angle = Math.atan2(y, x);
            x = Math.cos(angle) * maxRadius;
            y = Math.sin(angle) * maxRadius;
        }

        // mise à jour visuelle
        joystick.style.transform = `translate(${x}px, ${y}px)`;

        // Normaliser X,Y entre -1 et 1
        const normX = x / maxRadius;
        const normY = -y / maxRadius;

        fetch('/joystick', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ x: normX, y: normY })
        });
    };

    const handleMouseUp = () => {
        joystick.style.transform = 'translate(-50%, -50%)';

        // Stop
        fetch('/joystick', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ x: 0, y: 0 })
        });

        document.removeEventListener('mousemove', handleMouseMove);
        document.removeEventListener('mouseup', handleMouseUp);
    };

    document.addEventListener('mousemove', handleMouseMove);
    document.addEventListener('mouseup', handleMouseUp);
});